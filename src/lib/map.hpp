// map.hpp — Simple open-addressing hash map<K,V> for this freestanding
// RISC-V environment. No standard library dependencies.

#ifndef MAP_HPP
#define MAP_HPP

#include "types.hpp"
#include "heap.hpp"

// ── map<K,V>: simple open-addressing hash map using the virtual heap ──
template<typename K, typename V>
class map {
    struct Slot {
        K key;
        V val;
        bool used;   // true if this slot is occupied (not free and not tombstone)
        bool tomb;   // true if this slot was erased (probe chain continues past it)
    };

    Slot* d;
    unsigned int sz;     // number of live entries
    unsigned int cap;    // total capacity (always a power of 2)

    // Simple integer hash (Fowler–Noll–Vo 1a on raw bytes of key)
    static unsigned int _hash(const K& key) {
        const unsigned char* p = (const unsigned char*)&key;
        unsigned int h = 2166136261u;
        for (unsigned int i = 0; i < sizeof(K); i++) {
            h ^= (unsigned int)p[i];
            h *= 16777619u;
        }
        return h;
    }

    // Returns slot index for key (probes linearly). If key not found,
    // returns the first free or tombstone slot (or cap if table full).
    unsigned int _find_slot(const K& key, bool want_free) const {
        unsigned int idx = _hash(key) & (cap - 1);
        unsigned int first_tomb = cap;
        for (unsigned int i = 0; i < cap; i++) {
            if (!d[idx].used) {
                if (d[idx].tomb) {
                    if (first_tomb == cap) first_tomb = idx;
                    idx = (idx + 1) & (cap - 1);
                    continue;
                }
                // true free slot
                if (want_free) return (first_tomb != cap) ? first_tomb : idx;
                return cap;
            }
            if (d[idx].key == key) return idx;  // found
            idx = (idx + 1) & (cap - 1);
        }
        return cap;  // full / not found
    }

    void _grow() {
        unsigned int oldcap = cap;
        Slot* old = d;
        cap = cap ? cap * 2 : 8;
        sz = 0;
        d = (Slot*)Rbxl::malloc(cap * sizeof(Slot));
        for (unsigned int i = 0; i < cap; i++) {
            d[i].used = false;
            d[i].tomb = false;
        }
        for (unsigned int i = 0; i < oldcap; i++) {
            if (old[i].used) {
                unsigned int idx = _find_slot(old[i].key, true);
                d[idx].key = old[i].key;
                d[idx].val = old[i].val;
                d[idx].used = true;
                d[idx].tomb = false;
                sz++;
            }
        }
        if (old) Rbxl::free(old);
    }

public:
    map() : d(nullptr), sz(0), cap(0) {}
    ~map() { if (d) Rbxl::free(d); }

    // ── Capacity ──
    unsigned int size() const { return sz; }
    bool empty() const { return sz == 0; }

    // ── Lookup ──
    bool contains(const K& key) const {
        if (cap == 0) return false;
        return _find_slot(key, false) != cap;
    }

    // Returns pointer to value, or nullptr if key not found
    V* find(const K& key) {
        if (cap == 0) return nullptr;
        unsigned int idx = _find_slot(key, false);
        return (idx != cap) ? &d[idx].val : nullptr;
    }

    const V* find(const K& key) const {
        if (cap == 0) return nullptr;
        unsigned int idx = _find_slot(key, false);
        return (idx != cap) ? &d[idx].val : nullptr;
    }

    // ── Element access (inserts default if key missing) ──
    V& operator[](const K& key) {
        if (cap == 0 || sz * 2 >= cap) _grow();
        unsigned int idx = _find_slot(key, true);
        if (d[idx].used && d[idx].key == key) return d[idx].val;
        d[idx].key = key;
        d[idx].val = V();
        d[idx].used = true;
        d[idx].tomb = false;
        sz++;
        return d[idx].val;
    }

    // ── Insert ──
    void insert(const K& key, const V& value) {
        if (cap == 0 || sz * 2 >= cap) _grow();
        unsigned int idx = _find_slot(key, true);
        if (d[idx].used && d[idx].key == key) {
            d[idx].val = value;  // overwrite
        } else {
            d[idx].key = key;
            d[idx].val = value;
            d[idx].used = true;
            d[idx].tomb = false;
            sz++;
        }
    }

    // ── Erase ──
    void erase(const K& key) {
        if (cap == 0) return;
        unsigned int idx = _find_slot(key, false);
        if (idx != cap && d[idx].used) {
            d[idx].used = false;
            d[idx].tomb = true;
            sz--;
        }
    }

    // ── Clear ──
    void clear() {
        for (unsigned int i = 0; i < cap; i++) {
            d[i].used = false;
            d[i].tomb = false;
        }
        sz = 0;
    }
};

#endif // MAP_HPP
