	.file	"main_image.cpp"
	.option nopic
	.attribute arch, "rv32i2p1_m2p0_f2p2_zicsr2p0_zmmul1p0"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.section	.rodata.str1.4,"aMS",@progbits,1
	.align	2
.LC0:
	.string	"Workspace"
	.text
	.align	2
	.type	_ZN4Rbxl10getServiceEPKc.constprop.0, @function
_ZN4Rbxl10getServiceEPKc.constprop.0:
	lui	a5,%hi(.LC0)
	addi	a5,a5,%lo(.LC0)
 #APP
# 388 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 47; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl10getServiceEPKc.constprop.0, .-_ZN4Rbxl10getServiceEPKc.constprop.0
	.align	2
	.type	_ZN7Vector3C2Efff.constprop.0, @function
_ZN7Vector3C2Efff.constprop.0:
	lui	a5,%hi(.LC1)
	flw	fa5,%lo(.LC1)(a5)
	sw	a1,0(a0)
	sw	a2,4(a0)
	fsw	fa5,8(a0)
	ret
	.size	_ZN7Vector3C2Efff.constprop.0, .-_ZN7Vector3C2Efff.constprop.0
	.align	2
	.type	_ZN4math3radEf.constprop.0, @function
_ZN4math3radEf.constprop.0:
	lui	a5,%hi(.LC2)
	flw	fa5,%lo(.LC2)(a5)
	addi	sp,sp,-16
	addi	a5,sp,12
	fsw	fa5,12(sp)
 #APP
# 17 "../src/lib/math.hpp" 1
	mv a0, a5; li a7, 39; ecall
# 0 "" 2
 #NO_APP
	lw	a0,12(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN4math3radEf.constprop.0, .-_ZN4math3radEf.constprop.0
	.align	2
	.type	_ZN4math3radEf.constprop.1, @function
_ZN4math3radEf.constprop.1:
	lui	a5,%hi(.LC3)
	flw	fa5,%lo(.LC3)(a5)
	addi	sp,sp,-16
	addi	a5,sp,12
	fsw	fa5,12(sp)
 #APP
# 17 "../src/lib/math.hpp" 1
	mv a0, a5; li a7, 39; ecall
# 0 "" 2
 #NO_APP
	lw	a0,12(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN4math3radEf.constprop.1, .-_ZN4math3radEf.constprop.1
	.align	2
	.type	_ZN6vectorIhEixEj.isra.0, @function
_ZN6vectorIhEixEj.isra.0:
	add	a0,a0,a1
	ret
	.size	_ZN6vectorIhEixEj.isra.0, .-_ZN6vectorIhEixEj.isra.0
	.align	2
	.type	_ZNK6vectorIhEixEj.isra.0, @function
_ZNK6vectorIhEixEj.isra.0:
	add	a0,a0,a1
	ret
	.size	_ZNK6vectorIhEixEj.isra.0, .-_ZNK6vectorIhEixEj.isra.0
	.align	2
	.type	_ZNK6vectorIhE4sizeEv.isra.0, @function
_ZNK6vectorIhE4sizeEv.isra.0:
	ret
	.size	_ZNK6vectorIhE4sizeEv.isra.0, .-_ZNK6vectorIhE4sizeEv.isra.0
	.align	2
	.type	_ZNK6LuaObj5validEv.isra.0, @function
_ZNK6LuaObj5validEv.isra.0:
	snez	a0,a0
	ret
	.size	_ZNK6LuaObj5validEv.isra.0, .-_ZNK6LuaObj5validEv.isra.0
	.align	2
	.globl	__cxa_atexit
	.type	__cxa_atexit, @function
__cxa_atexit:
	li	a0,0
	ret
	.size	__cxa_atexit, .-__cxa_atexit
	.section	.text._ZN4math3radEf,"axG",@progbits,_ZN4math3radEf,comdat
	.align	2
	.weak	_ZN4math3radEf
	.type	_ZN4math3radEf, @function
_ZN4math3radEf:
	addi	sp,sp,-16
	addi	a5,sp,12
	sw	a0,12(sp)
 #APP
# 17 "../src/lib/math.hpp" 1
	mv a0, a5; li a7, 39; ecall
# 0 "" 2
 #NO_APP
	lw	a0,12(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN4math3radEf, .-_ZN4math3radEf
	.section	.text._ZN4math3sinEf,"axG",@progbits,_ZN4math3sinEf,comdat
	.align	2
	.weak	_ZN4math3sinEf
	.type	_ZN4math3sinEf, @function
_ZN4math3sinEf:
	addi	sp,sp,-16
	addi	a5,sp,12
	sw	a0,12(sp)
 #APP
# 25 "../src/lib/math.hpp" 1
	mv a0, a5; li a7, 40; ecall
# 0 "" 2
 #NO_APP
	lw	a0,12(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN4math3sinEf, .-_ZN4math3sinEf
	.section	.text._ZN4math3cosEf,"axG",@progbits,_ZN4math3cosEf,comdat
	.align	2
	.weak	_ZN4math3cosEf
	.type	_ZN4math3cosEf, @function
_ZN4math3cosEf:
	addi	sp,sp,-16
	addi	a5,sp,12
	sw	a0,12(sp)
 #APP
# 33 "../src/lib/math.hpp" 1
	mv a0, a5; li a7, 41; ecall
# 0 "" 2
 #NO_APP
	lw	a0,12(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN4math3cosEf, .-_ZN4math3cosEf
	.text
	.align	2
	.globl	_ZN4Rbxl6mallocEj
	.type	_ZN4Rbxl6mallocEj, @function
_ZN4Rbxl6mallocEj:
	mv	a5,a0
 #APP
# 15 "../src/lib/heap.hpp" 1
	mv a0, a5; li a7, 30; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl6mallocEj, .-_ZN4Rbxl6mallocEj
	.align	2
	.globl	_ZN4Rbxl4freeEPv
	.type	_ZN4Rbxl4freeEPv, @function
_ZN4Rbxl4freeEPv:
	mv	a5,a0
 #APP
# 26 "../src/lib/heap.hpp" 1
	mv a0, a5; li a7, 31; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN4Rbxl4freeEPv, .-_ZN4Rbxl4freeEPv
	.align	2
	.globl	_ZN4Rbxl8heapUsedEv
	.type	_ZN4Rbxl8heapUsedEv, @function
_ZN4Rbxl8heapUsedEv:
 #APP
# 37 "../src/lib/heap.hpp" 1
	li a7, 32; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl8heapUsedEv, .-_ZN4Rbxl8heapUsedEv
	.align	2
	.globl	_Z12decodeVarintRK6vectorIhERiPi
	.type	_Z12decodeVarintRK6vectorIhERiPi, @function
_Z12decodeVarintRK6vectorIhERiPi:
	addi	sp,sp,-32
	sw	s1,20(sp)
	sw	s2,16(sp)
	sw	s3,12(sp)
	sw	s4,8(sp)
	sw	s5,4(sp)
	sw	ra,28(sp)
	sw	s0,24(sp)
	mv	s4,a0
	mv	s3,a1
	mv	s5,a2
	li	s1,0
	li	s2,0
	j	.L23
.L25:
	lw	a0,0(s4)
	sw	a5,0(s3)
	call	_ZNK6vectorIhEixEj.isra.0
	lbu	a5,0(a0)
	lw	a4,0(s5)
	slli	a3,a5,24
	addi	a4,a4,1
	andi	a5,a5,127
	sll	a5,a5,s1
	srai	a3,a3,24
	sw	a4,0(s5)
	or	s2,s2,a5
	bge	a3,zero,.L22
	addi	s1,s1,7
.L23:
	lw	a0,4(s4)
	lw	s0,0(s3)
	call	_ZNK6vectorIhE4sizeEv.isra.0
	addi	a5,s0,1
	mv	a1,s0
	bltu	s0,a0,.L25
.L22:
	lw	ra,28(sp)
	lw	s0,24(sp)
	lw	s1,20(sp)
	lw	s3,12(sp)
	lw	s4,8(sp)
	lw	s5,4(sp)
	mv	a0,s2
	lw	s2,16(sp)
	addi	sp,sp,32
	jr	ra
	.size	_Z12decodeVarintRK6vectorIhERiPi, .-_Z12decodeVarintRK6vectorIhERiPi
	.section	.text._ZN3Lua5printEPKc,"axG",@progbits,_ZN3Lua5printEPKc,comdat
	.align	2
	.weak	_ZN3Lua5printEPKc
	.type	_ZN3Lua5printEPKc, @function
_ZN3Lua5printEPKc:
	mv	a5,a0
 #APP
# 31 "../src/lib/lua.hpp" 1
	mv a0, a5; li a7, 4; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN3Lua5printEPKc, .-_ZN3Lua5printEPKc
	.section	.rodata.str1.4
	.align	2
.LC4:
	.string	"Touched"
	.text
	.align	2
	.globl	_Z15touchedCallback6LuaObj
	.type	_Z15touchedCallback6LuaObj, @function
_Z15touchedCallback6LuaObj:
	lui	a0,%hi(.LC4)
	addi	a0,a0,%lo(.LC4)
	tail	_ZN3Lua5printEPKc
	.size	_Z15touchedCallback6LuaObj, .-_Z15touchedCallback6LuaObj
	.section	.text._ZN3Lua5printEi,"axG",@progbits,_ZN3Lua5printEi,comdat
	.align	2
	.weak	_ZN3Lua5printEi
	.type	_ZN3Lua5printEi, @function
_ZN3Lua5printEi:
	mv	a5,a0
 #APP
# 36 "../src/lib/lua.hpp" 1
	mv a0, a5; li a7, 5; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN3Lua5printEi, .-_ZN3Lua5printEi
	.section	.text._ZN3Lua5printEf,"axG",@progbits,_ZN3Lua5printEf,comdat
	.align	2
	.weak	_ZN3Lua5printEf
	.type	_ZN3Lua5printEf, @function
_ZN3Lua5printEf:
	addi	sp,sp,-16
	addi	a5,sp,12
	sw	a0,12(sp)
 #APP
# 48 "../src/lib/lua.hpp" 1
	mv a0, a5; li a7, 7; ecall
# 0 "" 2
 #NO_APP
	addi	sp,sp,16
	jr	ra
	.size	_ZN3Lua5printEf, .-_ZN3Lua5printEf
	.section	.text._ZN7Vector3C2Ev,"axG",@progbits,_ZN7Vector3C5Ev,comdat
	.align	2
	.weak	_ZN7Vector3C2Ev
	.type	_ZN7Vector3C2Ev, @function
_ZN7Vector3C2Ev:
	sw	zero,0(a0)
	sw	zero,4(a0)
	sw	zero,8(a0)
	ret
	.size	_ZN7Vector3C2Ev, .-_ZN7Vector3C2Ev
	.weak	_ZN7Vector3C1Ev
	.set	_ZN7Vector3C1Ev,_ZN7Vector3C2Ev
	.section	.text._ZN7Vector3C2Efff,"axG",@progbits,_ZN7Vector3C5Efff,comdat
	.align	2
	.weak	_ZN7Vector3C2Efff
	.type	_ZN7Vector3C2Efff, @function
_ZN7Vector3C2Efff:
	sw	a1,0(a0)
	sw	a2,4(a0)
	sw	a3,8(a0)
	ret
	.size	_ZN7Vector3C2Efff, .-_ZN7Vector3C2Efff
	.weak	_ZN7Vector3C1Efff
	.set	_ZN7Vector3C1Efff,_ZN7Vector3C2Efff
	.section	.text._ZN7Vector314readFromObjectEPv,"axG",@progbits,_ZN7Vector314readFromObjectEPv,comdat
	.align	2
	.weak	_ZN7Vector314readFromObjectEPv
	.type	_ZN7Vector314readFromObjectEPv, @function
_ZN7Vector314readFromObjectEPv:
	mv	a4,a0
	mv	a5,a1
 #APP
# 52 "../src/lib/rbxl.hpp" 1
	mv a0, a5; mv a1, a4; li a7, 54; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN7Vector314readFromObjectEPv, .-_ZN7Vector314readFromObjectEPv
	.section	.text._ZNK7Vector38toObjectEv,"axG",@progbits,_ZNK7Vector38toObjectEv,comdat
	.align	2
	.weak	_ZNK7Vector38toObjectEv
	.type	_ZNK7Vector38toObjectEv, @function
_ZNK7Vector38toObjectEv:
	mv	a5,a0
 #APP
# 62 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 55; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZNK7Vector38toObjectEv, .-_ZNK7Vector38toObjectEv
	.section	.text._ZN6Color3C2Efff,"axG",@progbits,_ZN6Color3C5Efff,comdat
	.align	2
	.weak	_ZN6Color3C2Efff
	.type	_ZN6Color3C2Efff, @function
_ZN6Color3C2Efff:
	sw	a1,0(a0)
	sw	a2,4(a0)
	sw	a3,8(a0)
	ret
	.size	_ZN6Color3C2Efff, .-_ZN6Color3C2Efff
	.weak	_ZN6Color3C1Efff
	.set	_ZN6Color3C1Efff,_ZN6Color3C2Efff
	.section	.text._ZNK6Color38toObjectEv,"axG",@progbits,_ZNK6Color38toObjectEv,comdat
	.align	2
	.weak	_ZNK6Color38toObjectEv
	.type	_ZNK6Color38toObjectEv, @function
_ZNK6Color38toObjectEv:
	mv	a5,a0
 #APP
# 89 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 59; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZNK6Color38toObjectEv, .-_ZNK6Color38toObjectEv
	.section	.text._ZNK6CFrame8toObjectEv,"axG",@progbits,_ZNK6CFrame8toObjectEv,comdat
	.align	2
	.weak	_ZNK6CFrame8toObjectEv
	.type	_ZNK6CFrame8toObjectEv, @function
_ZNK6CFrame8toObjectEv:
	mv	a5,a0
 #APP
# 152 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 57; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZNK6CFrame8toObjectEv, .-_ZNK6CFrame8toObjectEv
	.section	.text._ZN6CFrameC2Efff,"axG",@progbits,_ZN6CFrameC5Efff,comdat
	.align	2
	.weak	_ZN6CFrameC2Efff
	.type	_ZN6CFrameC2Efff, @function
_ZN6CFrameC2Efff:
	lui	a5,%hi(.LC5)
	flw	fa5,%lo(.LC5)(a5)
	sw	zero,16(a0)
	sw	zero,20(a0)
	sw	zero,24(a0)
	sw	zero,32(a0)
	sw	zero,36(a0)
	sw	zero,40(a0)
	sw	a1,0(a0)
	sw	a2,4(a0)
	sw	a3,8(a0)
	fsw	fa5,12(a0)
	fsw	fa5,28(a0)
	fsw	fa5,44(a0)
	ret
	.size	_ZN6CFrameC2Efff, .-_ZN6CFrameC2Efff
	.weak	_ZN6CFrameC1Efff
	.set	_ZN6CFrameC1Efff,_ZN6CFrameC2Efff
	.section	.text._ZN6CFrameC2Effffffffffff,"axG",@progbits,_ZN6CFrameC5Effffffffffff,comdat
	.align	2
	.weak	_ZN6CFrameC2Effffffffffff
	.type	_ZN6CFrameC2Effffffffffff, @function
_ZN6CFrameC2Effffffffffff:
	flw	fa1,0(sp)
	flw	fa2,4(sp)
	flw	fa3,8(sp)
	flw	fa4,12(sp)
	flw	fa5,16(sp)
	sw	a1,0(a0)
	sw	a2,4(a0)
	sw	a3,8(a0)
	sw	a4,12(a0)
	sw	a5,16(a0)
	sw	a6,20(a0)
	sw	a7,24(a0)
	fsw	fa1,28(a0)
	fsw	fa2,32(a0)
	fsw	fa3,36(a0)
	fsw	fa4,40(a0)
	fsw	fa5,44(a0)
	ret
	.size	_ZN6CFrameC2Effffffffffff, .-_ZN6CFrameC2Effffffffffff
	.weak	_ZN6CFrameC1Effffffffffff
	.set	_ZN6CFrameC1Effffffffffff,_ZN6CFrameC2Effffffffffff
	.section	.text._Z10cframe_mulRK6CFrameS1_,"axG",@progbits,_Z10cframe_mulRK6CFrameS1_,comdat
	.align	2
	.weak	_Z10cframe_mulRK6CFrameS1_
	.type	_Z10cframe_mulRK6CFrameS1_, @function
_Z10cframe_mulRK6CFrameS1_:
	flw	fa0,16(a1)
	flw	fa1,28(a1)
	flw	ft0,40(a1)
	flw	fa5,4(a2)
	flw	ft7,28(a2)
	flw	ft6,32(a2)
	fmul.s	fs0,fa0,fa5
	fmul.s	ft8,fa5,fa1
	fmul.s	fa5,fa5,ft0
	flw	fa6,24(a2)
	flw	fa4,12(a1)
	flw	fa7,0(a2)
	flw	fa3,24(a1)
	flw	fa2,36(a1)
	fmul.s	ft2,fa1,fa6
	fmul.s	ft1,ft0,ft6
	fmadd.s	ft9,fa7,fa2,fa5
	fmul.s	fs1,fa0,ft7
	fmul.s	ft5,fa1,ft7
	fmul.s	ft4,fa1,ft6
	fmul.s	ft3,ft0,fa6
	fmadd.s	fs0,fa4,fa7,fs0
	fmadd.s	ft8,fa7,fa3,ft8
	fmul.s	fa1,ft0,ft7
	fmul.s	fa7,fa0,fa6
	fmul.s	ft0,fa0,ft6
	flw	ft7,12(a2)
	flw	ft6,20(a2)
	flw	ft10,20(a1)
	flw	fa6,8(a2)
	flw	fa0,16(a2)
	flw	ft11,32(a1)
	flw	fa5,44(a1)
	fmadd.s	ft5,fa3,fa0,ft5
	fmadd.s	ft3,fa2,ft7,ft3
	fmadd.s	fa7,fa4,ft7,fa7
	fmadd.s	fs0,ft10,fa6,fs0
	fmadd.s	fa1,fa2,fa0,fa1
	fmadd.s	fa0,fa4,fa0,fs1
	fmadd.s	fa4,fa4,ft6,ft0
	flw	fs3,0(a1)
	fmadd.s	ft4,fa3,ft6,ft4
	fmadd.s	ft9,fa6,fa5,ft9
	fmadd.s	fa2,fa2,ft6,ft1
	fmadd.s	ft8,fa6,ft11,ft8
	flw	ft6,36(a2)
	flw	fa6,44(a2)
	flw	fs2,8(a1)
	fmadd.s	ft0,fa5,ft6,ft3
	fmadd.s	fa4,ft10,fa6,fa4
	fadd.s	ft3,fs0,fs3
	fmadd.s	fa3,fa3,ft7,ft2
	flw	ft7,40(a2)
	flw	fs1,4(a1)
	fmv.x.s	a6,fa4
	fmv.x.s	a1,ft3
	fmadd.s	fa4,ft10,ft7,fa0
	fadd.s	ft3,ft9,fs2
	fmadd.s	fa3,ft11,ft6,fa3
	fmadd.s	fa1,fa5,ft7,fa1
	fmadd.s	ft2,ft11,ft7,ft5
	fmv.x.s	a5,fa4
	fmv.x.s	a3,ft3
	fmadd.s	fa4,ft10,ft6,fa7
	fadd.s	ft3,ft8,fs1
	fmadd.s	ft1,ft11,fa6,ft4
	fmadd.s	fa5,fa5,fa6,fa2
	fmv.x.s	a7,fa3
	fmv.x.s	a4,fa4
	fmv.x.s	a2,ft3
	addi	sp,sp,-64
	sw	ra,60(sp)
	sw	a0,44(sp)
	fsw	ft2,0(sp)
	fsw	ft1,4(sp)
	fsw	ft0,8(sp)
	fsw	fa1,12(sp)
	fsw	fa5,16(sp)
	call	_ZN6CFrameC1Effffffffffff
	lw	ra,60(sp)
	lw	a0,44(sp)
	addi	sp,sp,64
	jr	ra
	.size	_Z10cframe_mulRK6CFrameS1_, .-_Z10cframe_mulRK6CFrameS1_
	.section	.text._Z22cframe_fromEulerAnglesfff,"axG",@progbits,_Z22cframe_fromEulerAnglesfff,comdat
	.align	2
	.weak	_Z22cframe_fromEulerAnglesfff
	.type	_Z22cframe_fromEulerAnglesfff, @function
_Z22cframe_fromEulerAnglesfff:
	addi	sp,sp,-80
	sw	s0,72(sp)
	mv	s0,a0
	mv	a0,a1
	sw	ra,76(sp)
	sw	s1,68(sp)
	sw	s2,64(sp)
	mv	s1,a3
	mv	s2,a2
	sw	a1,44(sp)
	call	_ZN4math3sinEf
	sw	a0,60(sp)
	lw	a0,44(sp)
	call	_ZN4math3cosEf
	sw	a0,56(sp)
	mv	a0,s2
	call	_ZN4math3sinEf
	sw	a0,52(sp)
	mv	a0,s2
	call	_ZN4math3cosEf
	sw	a0,48(sp)
	mv	a0,s1
	call	_ZN4math3sinEf
	sw	a0,44(sp)
	mv	a0,s1
	call	_ZN4math3cosEf
	flw	fa1,44(sp)
	fmv.s.x	fa2,a0
	flw	fa4,56(sp)
	flw	fa5,60(sp)
	flw	fa3,52(sp)
	fmul.s	ft4,fa4,fa1
	fmul.s	ft5,fa5,fa1
	fmul.s	ft3,fa4,fa3
	fmul.s	ft2,fa5,fa3
	fmul.s	ft1,fa5,fa2
	fmul.s	ft0,fa4,fa2
	flw	fa0,48(sp)
	fneg.s	fa3,fa3
	mv	a3,zero
	fmsub.s	ft1,ft3,fa1,ft1
	fmadd.s	ft0,ft2,fa1,ft0
	fmadd.s	ft3,ft3,fa2,ft5
	fmsub.s	ft2,ft2,fa2,ft4
	fmul.s	fa1,fa0,fa1
	fmul.s	fa2,fa0,fa2
	fmul.s	fa4,fa4,fa0
	fmul.s	fa5,fa5,fa0
	fmv.x.s	a6,ft3
	fmv.x.s	a5,ft2
	fmv.x.s	a7,fa1
	fmv.x.s	a4,fa2
	mv	a0,s0
	fsw	fa4,16(sp)
	fsw	fa5,12(sp)
	fsw	fa3,8(sp)
	fsw	ft1,4(sp)
	fsw	ft0,0(sp)
	mv	a2,a3
	mv	a1,a3
	call	_ZN6CFrameC1Effffffffffff
	lw	ra,76(sp)
	mv	a0,s0
	lw	s0,72(sp)
	lw	s1,68(sp)
	lw	s2,64(sp)
	addi	sp,sp,80
	jr	ra
	.size	_Z22cframe_fromEulerAnglesfff, .-_Z22cframe_fromEulerAnglesfff
	.text
	.align	2
	.globl	_ZN4Rbxl12createBufferEj
	.type	_ZN4Rbxl12createBufferEj, @function
_ZN4Rbxl12createBufferEj:
	mv	a5,a0
 #APP
# 270 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 21; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl12createBufferEj, .-_ZN4Rbxl12createBufferEj
	.align	2
	.globl	_ZN4Rbxl10freeBufferEPv
	.type	_ZN4Rbxl10freeBufferEPv, @function
_ZN4Rbxl10freeBufferEPv:
	mv	a5,a0
 #APP
# 276 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 22; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN4Rbxl10freeBufferEPv, .-_ZN4Rbxl10freeBufferEPv
	.align	2
	.globl	_ZN4Rbxl9bufferLenEPv
	.type	_ZN4Rbxl9bufferLenEPv, @function
_ZN4Rbxl9bufferLenEPv:
	mv	a5,a0
 #APP
# 282 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 23; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl9bufferLenEPv, .-_ZN4Rbxl9bufferLenEPv
	.align	2
	.globl	_ZN4Rbxl12bufferReadI8EPvj
	.type	_ZN4Rbxl12bufferReadI8EPvj, @function
_ZN4Rbxl12bufferReadI8EPvj:
	mv	a5,a0
	mv	a4,a1
 #APP
# 289 "../src/lib/rbxl.hpp" 1
	mv a0, a5; mv a1, a4; li a7, 24; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl12bufferReadI8EPvj, .-_ZN4Rbxl12bufferReadI8EPvj
	.align	2
	.globl	_ZN4Rbxl13bufferWriteI8EPvji
	.type	_ZN4Rbxl13bufferWriteI8EPvji, @function
_ZN4Rbxl13bufferWriteI8EPvji:
	mv	a5,a0
	mv	a4,a1
	mv	a3,a2
 #APP
# 295 "../src/lib/rbxl.hpp" 1
	mv a0, a5; mv a1, a4; mv a2, a3; li a7, 25; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN4Rbxl13bufferWriteI8EPvji, .-_ZN4Rbxl13bufferWriteI8EPvji
	.align	2
	.globl	_ZN4Rbxl13bufferReadI32EPvj
	.type	_ZN4Rbxl13bufferReadI32EPvj, @function
_ZN4Rbxl13bufferReadI32EPvj:
	mv	a5,a0
	mv	a4,a1
 #APP
# 301 "../src/lib/rbxl.hpp" 1
	mv a0, a5; mv a1, a4; li a7, 26; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl13bufferReadI32EPvj, .-_ZN4Rbxl13bufferReadI32EPvj
	.align	2
	.globl	_ZN4Rbxl14bufferWriteI32EPvji
	.type	_ZN4Rbxl14bufferWriteI32EPvji, @function
_ZN4Rbxl14bufferWriteI32EPvji:
	mv	a5,a0
	mv	a4,a1
	mv	a3,a2
 #APP
# 307 "../src/lib/rbxl.hpp" 1
	mv a0, a5; mv a1, a4; mv a2, a3; li a7, 27; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN4Rbxl14bufferWriteI32EPvji, .-_ZN4Rbxl14bufferWriteI32EPvji
	.align	2
	.globl	_ZN4Rbxl13bufferReadF32EPvj
	.type	_ZN4Rbxl13bufferReadF32EPvj, @function
_ZN4Rbxl13bufferReadF32EPvj:
	mv	a5,a0
	mv	a4,a1
 #APP
# 313 "../src/lib/rbxl.hpp" 1
	mv a0, a5; mv a1, a4; li a7, 28; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl13bufferReadF32EPvj, .-_ZN4Rbxl13bufferReadF32EPvj
	.align	2
	.globl	_ZN4Rbxl14bufferWriteF32EPvjf
	.type	_ZN4Rbxl14bufferWriteF32EPvjf, @function
_ZN4Rbxl14bufferWriteF32EPvjf:
	mv	a5,a0
	mv	a4,a1
	mv	a3,a2
 #APP
# 319 "../src/lib/rbxl.hpp" 1
	mv a0, a5; mv a1, a4; mv a2, a3; li a7, 29; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN4Rbxl14bufferWriteF32EPvjf, .-_ZN4Rbxl14bufferWriteF32EPvjf
	.align	2
	.globl	_ZN4Rbxl16bufferFromStringEPKc
	.type	_ZN4Rbxl16bufferFromStringEPKc, @function
_ZN4Rbxl16bufferFromStringEPKc:
	mv	a5,a0
 #APP
# 325 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 50; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl16bufferFromStringEPKc, .-_ZN4Rbxl16bufferFromStringEPKc
	.align	2
	.globl	_ZN4Rbxl3radEPv
	.type	_ZN4Rbxl3radEPv, @function
_ZN4Rbxl3radEPv:
	mv	a5,a0
 #APP
# 333 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 39; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN4Rbxl3radEPv, .-_ZN4Rbxl3radEPv
	.align	2
	.globl	_ZN4Rbxl3sinEPv
	.type	_ZN4Rbxl3sinEPv, @function
_ZN4Rbxl3sinEPv:
	mv	a5,a0
 #APP
# 338 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 40; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN4Rbxl3sinEPv, .-_ZN4Rbxl3sinEPv
	.align	2
	.globl	_ZN4Rbxl3cosEPv
	.type	_ZN4Rbxl3cosEPv, @function
_ZN4Rbxl3cosEPv:
	mv	a5,a0
 #APP
# 343 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 41; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN4Rbxl3cosEPv, .-_ZN4Rbxl3cosEPv
	.align	2
	.globl	_ZN4Rbxl17getPropertyObjectEPvPKc
	.type	_ZN4Rbxl17getPropertyObjectEPvPKc, @function
_ZN4Rbxl17getPropertyObjectEPvPKc:
	mv	a5,a0
	mv	a4,a1
 #APP
# 351 "../src/lib/rbxl.hpp" 1
	mv a0, a5; mv a1, a4; li a7, 62; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl17getPropertyObjectEPvPKc, .-_ZN4Rbxl17getPropertyObjectEPvPKc
	.align	2
	.globl	_ZN4Rbxl17setPropertyObjectEPvPKcS0_
	.type	_ZN4Rbxl17setPropertyObjectEPvPKcS0_, @function
_ZN4Rbxl17setPropertyObjectEPvPKcS0_:
	mv	a5,a0
	mv	a4,a1
	mv	a3,a2
 #APP
# 357 "../src/lib/rbxl.hpp" 1
	mv a0, a5; mv a1, a4; mv a2, a3; li a7, 63; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN4Rbxl17setPropertyObjectEPvPKcS0_, .-_ZN4Rbxl17setPropertyObjectEPvPKcS0_
	.align	2
	.globl	_ZN4Rbxl13releaseObjectEPv
	.type	_ZN4Rbxl13releaseObjectEPv, @function
_ZN4Rbxl13releaseObjectEPv:
	mv	a5,a0
 #APP
# 362 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 64; ecall
# 0 "" 2
 #NO_APP
	ret
	.size	_ZN4Rbxl13releaseObjectEPv, .-_ZN4Rbxl13releaseObjectEPv
	.align	2
	.globl	_ZN4Rbxl8fromEnumEi
	.type	_ZN4Rbxl8fromEnumEi, @function
_ZN4Rbxl8fromEnumEi:
	mv	a5,a0
 #APP
# 371 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 42; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl8fromEnumEi, .-_ZN4Rbxl8fromEnumEi
	.align	2
	.globl	_ZN4Rbxl6toEnumEPv
	.type	_ZN4Rbxl6toEnumEPv, @function
_ZN4Rbxl6toEnumEPv:
	mv	a5,a0
 #APP
# 379 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 43; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl6toEnumEPv, .-_ZN4Rbxl6toEnumEPv
	.align	2
	.globl	_ZN4Rbxl10getServiceEPKc
	.type	_ZN4Rbxl10getServiceEPKc, @function
_ZN4Rbxl10getServiceEPKc:
	mv	a5,a0
 #APP
# 388 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 47; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl10getServiceEPKc, .-_ZN4Rbxl10getServiceEPKc
	.align	2
	.globl	_ZN4Rbxl9getGlobalEPKc
	.type	_ZN4Rbxl9getGlobalEPKc, @function
_ZN4Rbxl9getGlobalEPKc:
	mv	a5,a0
 #APP
# 395 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 52; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl9getGlobalEPKc, .-_ZN4Rbxl9getGlobalEPKc
	.align	2
	.globl	_ZN4Rbxl9getMethodEPvPKc
	.type	_ZN4Rbxl9getMethodEPvPKc, @function
_ZN4Rbxl9getMethodEPvPKc:
	mv	a5,a0
	mv	a4,a1
 #APP
# 402 "../src/lib/rbxl.hpp" 1
	mv a0, a5; mv a1, a4; li a7, 51; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl9getMethodEPvPKc, .-_ZN4Rbxl9getMethodEPvPKc
	.align	2
	.globl	_ZN4Rbxl7requireEPv
	.type	_ZN4Rbxl7requireEPv, @function
_ZN4Rbxl7requireEPv:
	mv	a5,a0
 #APP
# 409 "../src/lib/rbxl.hpp" 1
	mv a0, a5; li a7, 53; ecall; mv a5, a0
# 0 "" 2
 #NO_APP
	mv	a0,a5
	ret
	.size	_ZN4Rbxl7requireEPv, .-_ZN4Rbxl7requireEPv
	.align	2
	.globl	_ZN4Rbxl4callEPvi
	.type	_ZN4Rbxl4callEPvi, @function
_ZN4Rbxl4callEPvi:
	mv	t1,a0
	mv	t3,a1
 #APP
# 419 "../src/lib/rbxl.hpp" 1
	mv a0, t1; mv a3, t3; mv a1, x0; mv a2, x0; mv a4, x0; mv a5, x0; mv a6, x0; li a7, 65; ecall; mv t1, a0
# 0 "" 2
 #NO_APP
	mv	a0,t1
	ret
	.size	_ZN4Rbxl4callEPvi, .-_ZN4Rbxl4callEPvi
	.align	2
	.type	_ZNK6LuaObj4callEi.isra.0, @function
_ZNK6LuaObj4callEi.isra.0:
	tail	_ZN4Rbxl4callEPvi
	.size	_ZNK6LuaObj4callEi.isra.0, .-_ZNK6LuaObj4callEi.isra.0
	.section	.text._ZN6LuaObjC2Ev,"axG",@progbits,_ZN6LuaObjC5Ev,comdat
	.align	2
	.weak	_ZN6LuaObjC2Ev
	.type	_ZN6LuaObjC2Ev, @function
_ZN6LuaObjC2Ev:
	sw	zero,0(a0)
	ret
	.size	_ZN6LuaObjC2Ev, .-_ZN6LuaObjC2Ev
	.weak	_ZN6LuaObjC1Ev
	.set	_ZN6LuaObjC1Ev,_ZN6LuaObjC2Ev
	.section	.text._ZN6LuaObjC2EPv,"axG",@progbits,_ZN6LuaObjC5EPv,comdat
	.align	2
	.weak	_ZN6LuaObjC2EPv
	.type	_ZN6LuaObjC2EPv, @function
_ZN6LuaObjC2EPv:
	sw	a1,0(a0)
	ret
	.size	_ZN6LuaObjC2EPv, .-_ZN6LuaObjC2EPv
	.weak	_ZN6LuaObjC1EPv
	.set	_ZN6LuaObjC1EPv,_ZN6LuaObjC2EPv
	.text
	.align	2
	.type	_ZN6LuaObj8fromBoolEb.constprop.0, @function
_ZN6LuaObj8fromBoolEb.constprop.0:
	addi	sp,sp,-16
	sw	s0,8(sp)
	sw	ra,12(sp)
	mv	s0,a0
	li	a1,1
 #APP
# 596 "../src/lib/rbxl.hpp" 1
	mv a0, a1; li a7, 68; ecall; mv a1, a0
# 0 "" 2
 #NO_APP
	mv	a0,s0
	call	_ZN6LuaObjC1EPv
	lw	ra,12(sp)
	mv	a0,s0
	lw	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN6LuaObj8fromBoolEb.constprop.0, .-_ZN6LuaObj8fromBoolEb.constprop.0
	.align	2
	.type	_ZN6LuaObj8fromEnumEi.constprop.0, @function
_ZN6LuaObj8fromEnumEi.constprop.0:
	addi	sp,sp,-16
	sw	s0,8(sp)
	mv	s0,a0
	li	a0,1894
	sw	ra,12(sp)
	call	_ZN4Rbxl8fromEnumEi
	mv	a1,a0
	mv	a0,s0
	call	_ZN6LuaObjC1EPv
	lw	ra,12(sp)
	mv	a0,s0
	lw	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN6LuaObj8fromEnumEi.constprop.0, .-_ZN6LuaObj8fromEnumEi.constprop.0
	.align	2
	.type	_ZNK6LuaObj9getMethodEPKc.isra.0, @function
_ZNK6LuaObj9getMethodEPKc.isra.0:
	addi	sp,sp,-16
	mv	a5,a1
	sw	s0,8(sp)
	mv	a1,a2
	mv	s0,a0
	mv	a0,a5
	sw	ra,12(sp)
	call	_ZN4Rbxl9getMethodEPvPKc
	mv	a1,a0
	mv	a0,s0
	call	_ZN6LuaObjC1EPv
	lw	ra,12(sp)
	mv	a0,s0
	lw	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZNK6LuaObj9getMethodEPKc.isra.0, .-_ZNK6LuaObj9getMethodEPKc.isra.0
	.align	2
	.type	_ZNK6LuaObj17getPropertyObjectEPKc.isra.0, @function
_ZNK6LuaObj17getPropertyObjectEPKc.isra.0:
	addi	sp,sp,-16
	mv	a5,a1
	sw	s0,8(sp)
	mv	a1,a2
	mv	s0,a0
	mv	a0,a5
	sw	ra,12(sp)
	call	_ZN4Rbxl17getPropertyObjectEPvPKc
	mv	a1,a0
	mv	a0,s0
	call	_ZN6LuaObjC1EPv
	lw	ra,12(sp)
	mv	a0,s0
	lw	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZNK6LuaObj17getPropertyObjectEPKc.isra.0, .-_ZNK6LuaObj17getPropertyObjectEPKc.isra.0
	.section	.text._ZNK6LuaObj6handleEv,"axG",@progbits,_ZNK6LuaObj6handleEv,comdat
	.align	2
	.weak	_ZNK6LuaObj6handleEv
	.type	_ZNK6LuaObj6handleEv, @function
_ZNK6LuaObj6handleEv:
	lw	a0,0(a0)
	ret
	.size	_ZNK6LuaObj6handleEv, .-_ZNK6LuaObj6handleEv
	.section	.text._ZN6LuaObj7releaseEv,"axG",@progbits,_ZN6LuaObj7releaseEv,comdat
	.align	2
	.weak	_ZN6LuaObj7releaseEv
	.type	_ZN6LuaObj7releaseEv, @function
_ZN6LuaObj7releaseEv:
	lw	a4,0(a0)
	beq	a4,zero,.L86
	addi	sp,sp,-32
	sw	a0,12(sp)
	mv	a0,a4
	sw	ra,28(sp)
	call	_ZN4Rbxl13releaseObjectEPv
	lw	a5,12(sp)
	lw	ra,28(sp)
	sw	zero,0(a5)
	addi	sp,sp,32
	jr	ra
.L86:
	ret
	.size	_ZN6LuaObj7releaseEv, .-_ZN6LuaObj7releaseEv
	.section	.text._ZN6LuaObjD2Ev,"axG",@progbits,_ZN6LuaObjD5Ev,comdat
	.align	2
	.weak	_ZN6LuaObjD2Ev
	.type	_ZN6LuaObjD2Ev, @function
_ZN6LuaObjD2Ev:
	tail	_ZN6LuaObj7releaseEv
	.size	_ZN6LuaObjD2Ev, .-_ZN6LuaObjD2Ev
	.weak	_ZN6LuaObjD1Ev
	.set	_ZN6LuaObjD1Ev,_ZN6LuaObjD2Ev
	.text
	.align	2
	.type	_ZNK6LuaObj16callMethodStaticEPKci.isra.0, @function
_ZNK6LuaObj16callMethodStaticEPKci.isra.0:
	addi	sp,sp,-32
	mv	a5,a1
	sw	s0,24(sp)
	mv	a1,a0
	mv	s0,a2
	addi	a0,sp,12
	mv	a2,a5
	sw	ra,28(sp)
	call	_ZNK6LuaObj17getPropertyObjectEPKc.isra.0
	lw	a0,12(sp)
	ori	a1,s0,256
	call	_ZNK6LuaObj4callEi.isra.0
	addi	a0,sp,12
	call	_ZN6LuaObjD1Ev
	lw	ra,28(sp)
	lw	s0,24(sp)
	addi	sp,sp,32
	jr	ra
	.size	_ZNK6LuaObj16callMethodStaticEPKci.isra.0, .-_ZNK6LuaObj16callMethodStaticEPKci.isra.0
	.align	2
	.type	_ZN6LuaObjaSEOS_.isra.0, @function
_ZN6LuaObjaSEOS_.isra.0:
	beq	a0,a1,.L95
	addi	sp,sp,-32
	sw	ra,28(sp)
	sw	a1,8(sp)
	sw	a0,12(sp)
	call	_ZN6LuaObj7releaseEv
	lw	a1,8(sp)
	lw	a5,12(sp)
	lw	ra,28(sp)
	lw	a4,0(a1)
	sw	a4,0(a5)
	sw	zero,0(a1)
	addi	sp,sp,32
	jr	ra
.L95:
	ret
	.size	_ZN6LuaObjaSEOS_.isra.0, .-_ZN6LuaObjaSEOS_.isra.0
	.section	.text._ZN6LuaObj8fromEnumEi,"axG",@progbits,_ZN6LuaObj8fromEnumEi,comdat
	.align	2
	.weak	_ZN6LuaObj8fromEnumEi
	.type	_ZN6LuaObj8fromEnumEi, @function
_ZN6LuaObj8fromEnumEi:
	addi	sp,sp,-16
	sw	s0,8(sp)
	mv	s0,a0
	mv	a0,a1
	sw	ra,12(sp)
	call	_ZN4Rbxl8fromEnumEi
	mv	a1,a0
	mv	a0,s0
	call	_ZN6LuaObjC1EPv
	lw	ra,12(sp)
	mv	a0,s0
	lw	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN6LuaObj8fromEnumEi, .-_ZN6LuaObj8fromEnumEi
	.section	.text._ZN6LuaObj9fromFloatEf,"axG",@progbits,_ZN6LuaObj9fromFloatEf,comdat
	.align	2
	.weak	_ZN6LuaObj9fromFloatEf
	.type	_ZN6LuaObj9fromFloatEf, @function
_ZN6LuaObj9fromFloatEf:
	addi	sp,sp,-16
	sw	s0,8(sp)
	sw	ra,12(sp)
	mv	s0,a0
 #APP
# 586 "../src/lib/rbxl.hpp" 1
	mv a0, a1; li a7, 66; ecall; mv a1, a0
# 0 "" 2
 #NO_APP
	mv	a0,s0
	call	_ZN6LuaObjC1EPv
	lw	ra,12(sp)
	mv	a0,s0
	lw	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN6LuaObj9fromFloatEf, .-_ZN6LuaObj9fromFloatEf
	.section	.text._ZN6LuaObj10fromStringEPKc,"axG",@progbits,_ZN6LuaObj10fromStringEPKc,comdat
	.align	2
	.weak	_ZN6LuaObj10fromStringEPKc
	.type	_ZN6LuaObj10fromStringEPKc, @function
_ZN6LuaObj10fromStringEPKc:
	addi	sp,sp,-16
	sw	s0,8(sp)
	sw	ra,12(sp)
	mv	s0,a0
 #APP
# 601 "../src/lib/rbxl.hpp" 1
	mv a0, a1; li a7, 69; ecall; mv a1, a0
# 0 "" 2
 #NO_APP
	mv	a0,s0
	call	_ZN6LuaObjC1EPv
	lw	ra,12(sp)
	mv	a0,s0
	lw	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN6LuaObj10fromStringEPKc, .-_ZN6LuaObj10fromStringEPKc
	.section	.text._ZNK6LuaObj17setPropertyObjectEPKcRKS_,"axG",@progbits,_ZNK6LuaObj17setPropertyObjectEPKcRKS_,comdat
	.align	2
	.weak	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	.type	_ZNK6LuaObj17setPropertyObjectEPKcRKS_, @function
_ZNK6LuaObj17setPropertyObjectEPKcRKS_:
	addi	sp,sp,-32
	mv	a5,a0
	sw	s0,24(sp)
	lw	s0,0(a5)
	mv	a0,a2
	sw	ra,28(sp)
	sw	a1,12(sp)
	call	_ZNK6LuaObj6handleEv
	mv	a2,a0
	mv	a0,s0
	lw	s0,24(sp)
	lw	a1,12(sp)
	lw	ra,28(sp)
	addi	sp,sp,32
	tail	_ZN4Rbxl17setPropertyObjectEPvPKcS0_
	.size	_ZNK6LuaObj17setPropertyObjectEPKcRKS_, .-_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	.section	.text._ZN6LuaObj10getServiceEPKc,"axG",@progbits,_ZN6LuaObj10getServiceEPKc,comdat
	.align	2
	.weak	_ZN6LuaObj10getServiceEPKc
	.type	_ZN6LuaObj10getServiceEPKc, @function
_ZN6LuaObj10getServiceEPKc:
	addi	sp,sp,-16
	sw	s0,8(sp)
	mv	s0,a0
	mv	a0,a1
	sw	ra,12(sp)
	call	_ZN4Rbxl10getServiceEPKc
	mv	a1,a0
	mv	a0,s0
	call	_ZN6LuaObjC1EPv
	lw	ra,12(sp)
	mv	a0,s0
	lw	s0,8(sp)
	addi	sp,sp,16
	jr	ra
	.size	_ZN6LuaObj10getServiceEPKc, .-_ZN6LuaObj10getServiceEPKc
	.text
	.align	2
	.globl	_Z5delayi
	.type	_Z5delayi, @function
_Z5delayi:
	addi	sp,sp,-16
	sw	a0,12(sp)
	lw	a5,12(sp)
	ble	a5,zero,.L108
.L110:
	lw	a5,12(sp)
	addi	a5,a5,-1
	sw	a5,12(sp)
	lw	a5,12(sp)
	bgt	a5,zero,.L110
.L108:
	addi	sp,sp,16
	jr	ra
	.size	_Z5delayi, .-_Z5delayi
	.section	.text._ZN4Rbxl4callIPvEES1_S1_RKT_i,"axG",@progbits,_ZN4Rbxl4callIPvEES1_S1_RKT_i,comdat
	.align	2
	.weak	_ZN4Rbxl4callIPvEES1_S1_RKT_i
	.type	_ZN4Rbxl4callIPvEES1_S1_RKT_i, @function
_ZN4Rbxl4callIPvEES1_S1_RKT_i:
	lw	t3,0(a1)
	mv	t1,a0
	mv	t4,a2
 #APP
# 431 "../src/lib/rbxl.hpp" 1
	mv a0, t1; mv a1, t3; mv a3, t4; mv a2, x0; mv a4, x0; mv a5, x0; mv a6, x0; li a7, 65; ecall; mv t1, a0
# 0 "" 2
 #NO_APP
	mv	a0,t1
	ret
	.size	_ZN4Rbxl4callIPvEES1_S1_RKT_i, .-_ZN4Rbxl4callIPvEES1_S1_RKT_i
	.section	.text._ZN4Rbxl4callEPvRK6LuaObji,"axG",@progbits,_ZN4Rbxl4callEPvRK6LuaObji,comdat
	.align	2
	.weak	_ZN4Rbxl4callEPvRK6LuaObji
	.type	_ZN4Rbxl4callEPvRK6LuaObji, @function
_ZN4Rbxl4callEPvRK6LuaObji:
	addi	sp,sp,-48
	sw	s0,40(sp)
	mv	s0,a0
	mv	a0,a1
	sw	ra,44(sp)
	sw	a2,12(sp)
	call	_ZNK6LuaObj6handleEv
	lw	a2,12(sp)
	sw	a0,28(sp)
	addi	a1,sp,28
	mv	a0,s0
	call	_ZN4Rbxl4callIPvEES1_S1_RKT_i
	lw	ra,44(sp)
	lw	s0,40(sp)
	addi	sp,sp,48
	jr	ra
	.size	_ZN4Rbxl4callEPvRK6LuaObji, .-_ZN4Rbxl4callEPvRK6LuaObji
	.text
	.align	2
	.type	_ZNK6LuaObj4callIS_EEPvRKT_i.isra.0, @function
_ZNK6LuaObj4callIS_EEPvRKT_i.isra.0:
	tail	_ZN4Rbxl4callEPvRK6LuaObji
	.size	_ZNK6LuaObj4callIS_EEPvRKT_i.isra.0, .-_ZNK6LuaObj4callIS_EEPvRKT_i.isra.0
	.section	.rodata.str1.4
	.align	2
.LC6:
	.string	"new"
	.text
	.align	2
	.type	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.0.isra.0, @function
_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.0.isra.0:
	addi	sp,sp,-32
	lui	a2,%hi(.LC6)
	sw	s0,24(sp)
	addi	a2,a2,%lo(.LC6)
	mv	s0,a1
	mv	a1,a0
	addi	a0,sp,12
	sw	ra,28(sp)
	call	_ZNK6LuaObj17getPropertyObjectEPKc.isra.0
	lw	a0,12(sp)
	li	a2,131072
	mv	a1,s0
	addi	a2,a2,259
	call	_ZNK6LuaObj4callIS_EEPvRKT_i.isra.0
	mv	s0,a0
	addi	a0,sp,12
	call	_ZN6LuaObjD1Ev
	lw	ra,28(sp)
	mv	a0,s0
	lw	s0,24(sp)
	addi	sp,sp,32
	jr	ra
	.size	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.0.isra.0, .-_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.0.isra.0
	.section	.rodata.str1.4
	.align	2
.LC7:
	.string	"wait"
	.text
	.align	2
	.type	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.1.isra.0, @function
_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.1.isra.0:
	addi	sp,sp,-32
	lui	a2,%hi(.LC7)
	sw	s0,24(sp)
	addi	a2,a2,%lo(.LC7)
	mv	s0,a1
	mv	a1,a0
	addi	a0,sp,12
	sw	ra,28(sp)
	call	_ZNK6LuaObj17getPropertyObjectEPKc.isra.0
	lw	a0,12(sp)
	li	a2,131072
	mv	a1,s0
	addi	a2,a2,256
	call	_ZNK6LuaObj4callIS_EEPvRKT_i.isra.0
	addi	a0,sp,12
	call	_ZN6LuaObjD1Ev
	lw	ra,28(sp)
	lw	s0,24(sp)
	addi	sp,sp,32
	jr	ra
	.size	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.1.isra.0, .-_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.1.isra.0
	.section	.rodata.str1.4
	.align	2
.LC8:
	.string	"task"
	.align	2
.LC9:
	.string	"Thread"
	.text
	.align	2
	.globl	_Z9printFunci
	.type	_Z9printFunci, @function
_Z9printFunci:
	addi	sp,sp,-48
	lui	a5,%hi(.LC8)
	sw	s4,24(sp)
	mv	s4,a0
	addi	a0,a5,%lo(.LC8)
	sw	ra,44(sp)
	sw	s0,40(sp)
	sw	s1,36(sp)
	sw	s2,32(sp)
	sw	s3,28(sp)
	call	_ZN4Rbxl9getGlobalEPKc
	mv	a1,a0
	addi	a0,sp,8
	call	_ZN6LuaObjC1EPv
	lui	a5,%hi(.LC5)
	lw	a1,%lo(.LC5)(a5)
	addi	a0,sp,12
	lui	s1,%hi(.LC9)
	call	_ZN6LuaObj9fromFloatEf
	lw	s3,8(sp)
	addi	s1,s1,%lo(.LC9)
	li	s0,0
	li	s2,10
.L122:
	mv	a0,s1
	call	_ZN3Lua5printEPKc
	mv	a0,s4
	call	_ZN3Lua5printEi
	mv	a0,s0
	call	_ZN3Lua5printEi
	addi	a1,sp,12
	mv	a0,s3
	addi	s0,s0,1
	call	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.1.isra.0
	bne	s0,s2,.L122
	addi	a0,sp,12
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,8
	call	_ZN6LuaObjD1Ev
	lw	ra,44(sp)
	lw	s0,40(sp)
	lw	s1,36(sp)
	lw	s2,32(sp)
	lw	s3,28(sp)
	lw	s4,24(sp)
	addi	sp,sp,48
	jr	ra
	.size	_Z9printFunci, .-_Z9printFunci
	.section	.text._ZN4Rbxl4callIPvS1_EES1_S1_RKT_RKT0_i,"axG",@progbits,_ZN4Rbxl4callIPvS1_EES1_S1_RKT_RKT0_i,comdat
	.align	2
	.weak	_ZN4Rbxl4callIPvS1_EES1_S1_RKT_RKT0_i
	.type	_ZN4Rbxl4callIPvS1_EES1_S1_RKT_RKT0_i, @function
_ZN4Rbxl4callIPvS1_EES1_S1_RKT_RKT0_i:
	lw	t3,0(a1)
	lw	t4,0(a2)
	mv	t1,a0
	mv	t5,a3
 #APP
# 443 "../src/lib/rbxl.hpp" 1
	mv a0, t1; mv a1, t3; mv a2, t4; mv a3, t5; mv a4, x0; mv a5, x0; mv a6, x0; li a7, 65; ecall; mv t1, a0
# 0 "" 2
 #NO_APP
	mv	a0,t1
	ret
	.size	_ZN4Rbxl4callIPvS1_EES1_S1_RKT_RKT0_i, .-_ZN4Rbxl4callIPvS1_EES1_S1_RKT_RKT0_i
	.section	.text._ZNK6LuaObj4callIPvS1_EES1_RKT_RKT0_i.isra.0,"axG",@progbits,_ZNK6LuaObj10callMethodIPvEES1_PKcRKT_i,comdat
	.align	2
	.type	_ZNK6LuaObj4callIPvS1_EES1_RKT_RKT0_i.isra.0, @function
_ZNK6LuaObj4callIPvS1_EES1_RKT_RKT0_i.isra.0:
	tail	_ZN4Rbxl4callIPvS1_EES1_S1_RKT_RKT0_i
	.size	_ZNK6LuaObj4callIPvS1_EES1_RKT_RKT0_i.isra.0, .-_ZNK6LuaObj4callIPvS1_EES1_RKT_RKT0_i.isra.0
	.section	.text._ZNK6LuaObj10callMethodIPvEES1_PKcRKT_i,"axG",@progbits,_ZNK6LuaObj10callMethodIPvEES1_PKcRKT_i,comdat
	.align	2
	.weak	_ZNK6LuaObj10callMethodIPvEES1_PKcRKT_i
	.type	_ZNK6LuaObj10callMethodIPvEES1_PKcRKT_i, @function
_ZNK6LuaObj10callMethodIPvEES1_PKcRKT_i:
	mv	a5,a1
	lw	a1,0(a0)
	addi	sp,sp,-48
	sw	s0,40(sp)
	sw	s1,36(sp)
	mv	s0,a0
	mv	s1,a2
	addi	a0,sp,28
	mv	a2,a5
	sw	ra,44(sp)
	sw	a3,12(sp)
	call	_ZNK6LuaObj17getPropertyObjectEPKc.isra.0
	lw	a3,12(sp)
	lw	a0,28(sp)
	li	a5,2097152
	mv	a2,s1
	mv	a1,s0
	or	a3,a3,a5
	call	_ZNK6LuaObj4callIPvS1_EES1_RKT_RKT0_i.isra.0
	mv	s0,a0
	addi	a0,sp,28
	call	_ZN6LuaObjD1Ev
	lw	ra,44(sp)
	mv	a0,s0
	lw	s0,40(sp)
	lw	s1,36(sp)
	addi	sp,sp,48
	jr	ra
	.size	_ZNK6LuaObj10callMethodIPvEES1_PKcRKT_i, .-_ZNK6LuaObj10callMethodIPvEES1_PKcRKT_i
	.section	.text._ZN6vectorIhE5clearEv,"axG",@progbits,_ZN6vectorIhE5clearEv,comdat
	.align	2
	.weak	_ZN6vectorIhE5clearEv
	.type	_ZN6vectorIhE5clearEv, @function
_ZN6vectorIhE5clearEv:
	sw	zero,4(a0)
	ret
	.size	_ZN6vectorIhE5clearEv, .-_ZN6vectorIhE5clearEv
	.section	.text._ZN6vectorIhE9push_backERKh,"axG",@progbits,_ZN6vectorIhE9push_backERKh,comdat
	.align	2
	.weak	_ZN6vectorIhE9push_backERKh
	.type	_ZN6vectorIhE9push_backERKh, @function
_ZN6vectorIhE9push_backERKh:
	lw	a4,4(a0)
	lw	a5,8(a0)
	mv	a3,a0
	bgeu	a4,a5,.L131
	lw	a2,0(a0)
	lbu	a5,0(a1)
	add	a2,a2,a4
	sb	a5,0(a2)
	lw	a5,4(a0)
	addi	a5,a5,1
	sw	a5,4(a0)
	ret
.L131:
	addi	sp,sp,-48
	sw	ra,44(sp)
	li	a6,4
	beq	a5,zero,.L133
	slli	a6,a5,1
.L133:
	mv	a0,a6
	sw	a1,24(sp)
	sw	a3,20(sp)
	sw	a4,16(sp)
	sw	a6,12(sp)
	call	_ZN4Rbxl6mallocEj
	lw	a4,16(sp)
	lw	a6,12(sp)
	lw	a3,20(sp)
	lw	a1,24(sp)
	mv	a2,a0
	beq	a4,zero,.L134
	li	a5,0
.L135:
	lw	a4,0(a3)
	add	a0,a2,a5
	add	a4,a4,a5
	lbu	a4,0(a4)
	addi	a5,a5,1
	sb	a4,0(a0)
	lw	a4,4(a3)
	bgtu	a4,a5,.L135
.L134:
	lw	a0,0(a3)
	beq	a0,zero,.L136
	sw	a1,28(sp)
	sw	a3,24(sp)
	sw	a2,20(sp)
	sw	a6,16(sp)
	sw	a4,12(sp)
	call	_ZN4Rbxl4freeEPv
	lw	a1,28(sp)
	lw	a3,24(sp)
	lw	a2,20(sp)
	lw	a6,16(sp)
	lw	a4,12(sp)
.L136:
	sw	a2,0(a3)
	sw	a6,8(a3)
	lbu	a5,0(a1)
	add	a2,a2,a4
	sb	a5,0(a2)
	lw	a5,4(a3)
	lw	ra,44(sp)
	addi	a5,a5,1
	sw	a5,4(a3)
	addi	sp,sp,48
	jr	ra
	.size	_ZN6vectorIhE9push_backERKh, .-_ZN6vectorIhE9push_backERKh
	.section	.rodata.str1.4
	.align	2
.LC10:
	.string	"Call to base64 decode"
	.align	2
.LC11:
	.string	"EncodingService"
	.align	2
.LC12:
	.string	"Base64Decode"
	.align	2
.LC13:
	.string	"Reading buffer into vector"
	.align	2
.LC14:
	.string	"The length of the buffer is:"
	.text
	.align	2
	.type	_Z13base64_decodePKcR6vectorIhE.isra.0, @function
_Z13base64_decodePKcR6vectorIhE.isra.0:
	addi	sp,sp,-48
	lui	a5,%hi(.LC10)
	sw	s0,40(sp)
	mv	s0,a0
	addi	a0,a5,%lo(.LC10)
	sw	s3,28(sp)
	sw	ra,44(sp)
	mv	s3,a1
	call	_ZN3Lua5printEPKc
	beq	s0,zero,.L149
	lbu	a5,0(s0)
	beq	a5,zero,.L149
	sw	s2,32(sp)
	lui	s2,%hi(_ZGVZ13base64_decodePKcR6vectorIhEE11encodingSvc)
	lbu	a5,%lo(_ZGVZ13base64_decodePKcR6vectorIhEE11encodingSvc)(s2)
	sw	s1,36(sp)
	lui	s1,%hi(_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc)
	beq	a5,zero,.L167
.L151:
	lw	a0,%lo(_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc)(s1)
	call	_ZNK6LuaObj5validEv.isra.0
	beq	a0,zero,.L169
.L152:
	mv	a0,s0
	call	_ZN4Rbxl16bufferFromStringEPKc
	lui	a1,%hi(.LC12)
	addi	a2,sp,12
	addi	a1,a1,%lo(.LC12)
	li	a3,545
	sw	a0,12(sp)
	addi	a0,s1,%lo(_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc)
	call	_ZNK6LuaObj10callMethodIPvEES1_PKcRKT_i
	mv	s1,a0
	lui	a0,%hi(.LC13)
	addi	a0,a0,%lo(.LC13)
	call	_ZN3Lua5printEPKc
	mv	a0,s1
	call	_ZN4Rbxl9bufferLenEPv
	mv	s2,a0
	lui	a0,%hi(.LC14)
	addi	a0,a0,%lo(.LC14)
	call	_ZN3Lua5printEPKc
	mv	a0,s2
	call	_ZN3Lua5printEi
	mv	a0,s3
	call	_ZN6vectorIhE5clearEv
	beq	s2,zero,.L153
	li	s0,0
.L154:
	mv	a1,s0
	mv	a0,s1
	call	_ZN4Rbxl12bufferReadI8EPvj
	sb	a0,12(sp)
	addi	a1,sp,12
	mv	a0,s3
	addi	s0,s0,1
	call	_ZN6vectorIhE9push_backERKh
	bne	s2,s0,.L154
.L153:
	lw	s0,40(sp)
	lw	s2,32(sp)
	lw	ra,44(sp)
	lw	s3,28(sp)
	mv	a0,s1
	lw	s1,36(sp)
	addi	sp,sp,48
	tail	_ZN4Rbxl10freeBufferEPv
.L149:
	lw	ra,44(sp)
	lw	s0,40(sp)
	lw	s3,28(sp)
	addi	sp,sp,48
	jr	ra
.L169:
	lui	a1,%hi(.LC11)
	addi	a0,sp,12
	addi	a1,a1,%lo(.LC11)
	call	_ZN6LuaObj10getServiceEPKc
	addi	a0,s1,%lo(_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc)
	addi	a1,sp,12
	call	_ZN6LuaObjaSEOS_.isra.0
	addi	a0,sp,12
	call	_ZN6LuaObjD1Ev
	j	.L152
.L167:
	addi	a0,s1,%lo(_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc)
	call	_ZN6LuaObjC1Ev
	lui	a2,%hi(__dso_handle)
	lui	a0,%hi(_ZN6LuaObjD1Ev)
	li	a5,1
	addi	a1,s1,%lo(_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc)
	addi	a2,a2,%lo(__dso_handle)
	addi	a0,a0,%lo(_ZN6LuaObjD1Ev)
	sb	a5,%lo(_ZGVZ13base64_decodePKcR6vectorIhEE11encodingSvc)(s2)
	call	__cxa_atexit
	j	.L151
	.size	_Z13base64_decodePKcR6vectorIhE.isra.0, .-_Z13base64_decodePKcR6vectorIhE.isra.0
	.section	.text._ZN6vectorIhEC2Ev,"axG",@progbits,_ZN6vectorIhEC5Ev,comdat
	.align	2
	.weak	_ZN6vectorIhEC2Ev
	.type	_ZN6vectorIhEC2Ev, @function
_ZN6vectorIhEC2Ev:
	sw	zero,0(a0)
	sw	zero,4(a0)
	sw	zero,8(a0)
	ret
	.size	_ZN6vectorIhEC2Ev, .-_ZN6vectorIhEC2Ev
	.weak	_ZN6vectorIhEC1Ev
	.set	_ZN6vectorIhEC1Ev,_ZN6vectorIhEC2Ev
	.section	.text._ZN6vectorIhED2Ev,"axG",@progbits,_ZN6vectorIhED5Ev,comdat
	.align	2
	.weak	_ZN6vectorIhED2Ev
	.type	_ZN6vectorIhED2Ev, @function
_ZN6vectorIhED2Ev:
	lw	a0,0(a0)
	beq	a0,zero,.L171
	tail	_ZN4Rbxl4freeEPv
.L171:
	ret
	.size	_ZN6vectorIhED2Ev, .-_ZN6vectorIhED2Ev
	.weak	_ZN6vectorIhED1Ev
	.set	_ZN6vectorIhED1Ev,_ZN6vectorIhED2Ev
	.section	.text._ZN4Rbxl4callIPvEES1_S1_RKT_RK6LuaObji,"axG",@progbits,_ZN4Rbxl4callIPvEES1_S1_RKT_RK6LuaObji,comdat
	.align	2
	.weak	_ZN4Rbxl4callIPvEES1_S1_RKT_RK6LuaObji
	.type	_ZN4Rbxl4callIPvEES1_S1_RKT_RK6LuaObji, @function
_ZN4Rbxl4callIPvEES1_S1_RKT_RK6LuaObji:
	addi	sp,sp,-48
	sw	s0,40(sp)
	mv	s0,a0
	mv	a0,a2
	sw	ra,44(sp)
	sw	a1,12(sp)
	sw	a3,8(sp)
	call	_ZNK6LuaObj6handleEv
	lw	a3,8(sp)
	lw	a1,12(sp)
	sw	a0,28(sp)
	addi	a2,sp,28
	mv	a0,s0
	call	_ZN4Rbxl4callIPvS1_EES1_S1_RKT_RKT0_i
	lw	ra,44(sp)
	lw	s0,40(sp)
	addi	sp,sp,48
	jr	ra
	.size	_ZN4Rbxl4callIPvEES1_S1_RKT_RK6LuaObji, .-_ZN4Rbxl4callIPvEES1_S1_RKT_RK6LuaObji
	.section	.text._ZNK6LuaObj4callIPvS_EES1_RKT_RKT0_i.isra.0,"axG",@progbits,_ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i,comdat
	.align	2
	.type	_ZNK6LuaObj4callIPvS_EES1_RKT_RKT0_i.isra.0, @function
_ZNK6LuaObj4callIPvS_EES1_RKT_RKT0_i.isra.0:
	tail	_ZN4Rbxl4callIPvEES1_S1_RKT_RK6LuaObji
	.size	_ZNK6LuaObj4callIPvS_EES1_RKT_RKT0_i.isra.0, .-_ZNK6LuaObj4callIPvS_EES1_RKT_RKT0_i.isra.0
	.section	.text._ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i,"axG",@progbits,_ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i,comdat
	.align	2
	.weak	_ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i
	.type	_ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i, @function
_ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i:
	mv	a5,a1
	lw	a1,0(a0)
	addi	sp,sp,-48
	sw	s0,40(sp)
	sw	s1,36(sp)
	mv	s0,a0
	mv	s1,a2
	addi	a0,sp,28
	mv	a2,a5
	sw	ra,44(sp)
	sw	a3,12(sp)
	call	_ZNK6LuaObj17getPropertyObjectEPKc.isra.0
	lw	a3,12(sp)
	lw	a0,28(sp)
	li	a5,2097152
	mv	a2,s1
	mv	a1,s0
	or	a3,a3,a5
	call	_ZNK6LuaObj4callIPvS_EES1_RKT_RKT0_i.isra.0
	mv	s0,a0
	addi	a0,sp,28
	call	_ZN6LuaObjD1Ev
	lw	ra,44(sp)
	mv	a0,s0
	lw	s0,40(sp)
	lw	s1,36(sp)
	addi	sp,sp,48
	jr	ra
	.size	_ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i, .-_ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i
	.section	.rodata.str1.4
	.align	2
.LC15:
	.string	"The start of the program"
	.align	2
.LC16:
	.string	"Version 4"
	.align	2
.LC17:
	.string	"ReplicatedStorage"
	.align	2
.LC18:
	.string	"Shared"
	.align	2
.LC19:
	.string	"Hello"
	.align	2
.LC20:
	.string	"FindFirstChild"
	.align	2
.LC21:
	.string	"require"
	.align	2
.LC22:
	.string	"Module already called!"
	.align	2
.LC23:
	.string	"Baseplate"
	.align	2
.LC24:
	.string	"Position"
	.align	2
.LC25:
	.string	"Position:"
	.align	2
.LC27:
	.string	"Connect"
	.align	2
.LC29:
	.string	"Finished wait! Doing work!"
	.align	2
.LC30:
	.ascii	"8ATeAgIADGwZ1gPHAuQCLF9tAAIBIscChQFVVQCHkmwBmgMW9ALAAlkRQlsA"
	.ascii	"3wL5ASEhABgrOwEDAsABAADRAesBKw04TgJgeqkB0AHjAip4kgDtAkjeAXph"
	.ascii	"IWiBALsDggHMAYYC5QEJIDQCuAJZKCgAybdpAfgC0AETEwAkOkoBtwQm4gFK"
	.ascii	"NAktRADnBFUGBgAid54B5QTZAQYGAB50oAHlBDgDAwAmZYYBxwQXAgIANmqK"
	.ascii	"AdkEOgICAC9njwHLBBYCAgArXnoBrwRtAgIAKVVwAewERQICACFefQHBBBsC"
	.ascii	"Aq0BOmJ7AN8ENQMDAAcxTgHDBBkCAgAMMU4BAwO4AiClAW1l2gELKjsC2QIB"
	.ascii	"nwFSxwIsYG0ClAGmASsrADefugGOApoCalQIJnqYAMYEmwEqKgALHSwB0AFS"
	.ascii	"XilcOY2hAJcEngI+PgAGGy0BW2YoKAAIITABfqACBwcARajDAYUDwAEGBgAi"
	.ascii	"Qk8BhwG3AgQEAFO60wGRBHIDBNYBUJi0AoIC5AECAgBgw90BhwLVAQICAFKp"
	.ascii	"ygHnBCUCAgAzYHgBfJACAgIAUpm2AeUE2QEDAwAsmcUB5QLHAQMD7AFlUEEC"
	.ascii	"5gRXBQUAIXqkAe0EBAZgtAEHK0QCggLuAQICAEKSrgHVBBoCAgAkSGQB/gHQ"
	.ascii	"AQICtAFfqcUA3gQfAwMAGDpWAeUEOQICADh7nAGuBGwCAo4BR3SOAJoCbgIC"
	.ascii	"jwLUw3kCcZQCAgKkAU+NpgCbAeIBAgIAR36YAQMEpAMFAKAELQANPVUA3gJW"
	.ascii	"MG5Ipp5iALABnAE9ngEBMZOwADOrAjMzAAMUIwGCA4QCXYIB4AIOL0cAXK0B"
	.ascii	"EBAANompAZUCigETEwAuhZ8BrwR/JKwBBAcYKACPAbUBFBQAQ73ZAeECxAIa"
	.ascii	"GgAtjqsBoQHWAQgIABU4TAGnArwCBAQAWcjdAZIBkQEFBQBf4fABwwKlAgMD"
	.ascii	"AH3Y5gF8dQwMAAczTwGqAX0ICAA1i6IBkAPDAQ4OACJVagGCAZsBCQkAJ42s"
	.ascii	"AYwBxQIMDAAsfpoBf4QCBwcAKXGMAagBywEDAwBluNcBeqMCAwMAY8jeAYAB"
	.ascii	"owIDAwBg0eQBe6cBBAQAJISiAXSNAgMDACpVaAGlAcEBCAO6AUG/2wCBAZsC"
	.ascii	"AwMARqzMAYIC4wECAgBhyOABlARzAgLAAnC0zwJ7jwICAjx3vNgAowKcAgIC"
	.ascii	"AD6YtQHuAqMCAgIANpi5AecEIwICgwFDcokA5gROCALcARVdfgLZBGZjD+wB"
	.ascii	"CS9JAOkEVwMDACqHtAHjBFgDAwAieaAB5QLHAQICwAJROwwClQHOAQICcFuo"
	.ascii	"zgADBYUFzQJN/gFDWB1xjwC7ArwBICAAwqJXAZ0COhQUAL6nZAEV2gL1ASHW"
	.ascii	"AhRDWwAhQiEhABBMaQHTAnYcHADavWEBcicnJwAFHS0B9AMlYTHaARddfQAu"
	.ascii	"zAEtLQAFEx8B4wEiHR0ABSlAAYUDngEVFQDSq1ABhwSgAmw95QIDDRoAAQXW"
	.ascii	"AhfwARZLYQIzvQKIAUCbAhREXgKpBLkBExMAI05gAdwCMhAQACRyjgHfAqUB"
	.ascii	"CAgAR2pvAf0CbgwMADiEkQFkrwEQEAA+o8YBywTsASYdUwo+YACDA5QCEBAA"
	.ascii	"CCU8AaQEANkCDvH/AwkhNACoBO0BGxsABSE3AdMCswIFBQBcw9QByALDAgxS"
	.ascii	"4gIyn78C0wKkAgkJACFXbgGcAcABCQkAUtHmAfYCuwIHBwBEq8UBjQGsAQsL"
	.ascii	"AE3R6wGAAcIBEwaEATKZuAKgAZUBBxmyAUO62QCXAdsBBgYAByQ7AfIBvAEE"
	.ascii	"BABCp8UB6wLTAgkJACR5mAGVA8QBAgIAeLTLAZYBzAICAgBqtswBpQHaAQID"
	.ascii	"8wE7epEAoAGFAQ0NADOfuwGLAcICAgIAXbTPAYEB6QECHd4BHk5mANwCwAID"
	.ascii	"AwBButQBlAGUAQQEAGzu9gGpAr0CAwMAat3uAcECpAICAgB73+sB9gKwAgQE"
	.ascii	"ADGWsQHnAcABAwMAR7rQAYoBvAIDAwAbZn0B4wKtAgICAFPD3wHaAqwCAgIA"
	.ascii	"Uq7MAXiHAgQEAC1VbQHfAskCAwMAN6nGAX+LAgICAFy0yQGOAckCBgYALIWi"
	.ascii	"AYMEBAICABdZegHZAsUCAwMAG32aAYMBnwIDAwA/sM8BpwHKAQICAHHN7gGu"
	.ascii	"AcIBAgIAQsPfAd4EUwUCgAEYZooCAwbQCMsDeU4eChA/WACrA6cBYTUNI4Ki"
	.ascii	"APgCMFkhtAEKOlMAxgMZE4kBjgInhqIAgwKjARUdhALGp2AAywFUICAABik/"
	.ascii	"AcsBqAEcHAA7qMIBAGIzav8BBhopAL8CayEhANvDZwEi6wFiHXUGHC0AuAGa"
	.ascii	"AjIyACyIpwEWyALnARS0AQwwRwJtAKACFrcBBilAAM8CwAEWFgDMpE8BiAKy"
	.ascii	"Ag0NABdGXwGYAucBMx83GUFWAIYCWwlwXy17kQL8AqsBEREAy6JNAZACMQoK"
	.ascii	"ALyeXQHmAsIC1QGfASUPMEQA3wM4CAgAOK7NAfMCfQcHAFJ8dgHNAp0BBQUA"
	.ascii	"VpWUAVurAisYmQIdYH4C3wTlAQUFACN9qwGJBAAXGzkGJDoCmATvARRg9gED"
	.ascii	"Dx4AsAQJEz6sAhVPbwBxvAEQEAA5nMABvwTdAlAqWwUcMAChBK0BCgoAMU9W"
	.ascii	"AfYD0gJjKlUDBw4CyQLTAgQEAFHJ6gGXBBYDAwA/n8MBmAQnAwMAN5m/AVO1"
	.ascii	"AQsH3AEvY4EA5QQLCwsABhYkAfACtAIDAwBSyeQB4gT2AQUFABZchAGRBPQB"
	.ascii	"BAQAEkdjAeMEiQIGBgATVH4BxwKvAggIABpqhwHfAqQCBQUANJOwAZ8BwwEE"
	.ascii	"BACC6fIB2gMUAwMAL5vDAdICtQIEBABo2OUBxQODAQMDADCbvAGmAYoBBAQA"
	.ascii	"PsHfAdoDHwMDADOdwwFbwgEDAwAhP1YB6gTnASoqiwIFMFAA0wKoAgMDACY4"
	.ascii	"PgGTA8IBAgIAQoahAdAE9QEGB5UBEE93AI8BpgEGBgBY3fIBjwGIAQYGADay"
	.ascii	"0AGVAbUBBAQAVuD2Ac0CxAIJCQAumbUBowGoAQcHAEW51AHqA5sBAgIATaS/"
	.ascii	"AdICPwICALWrfgHjBJsCDA5HAhkrAPQCvQIDAwBRz+kBoAG2AQYGADe31gHw"
	.ascii	"A5sBAwLJAUqguwD7ArMCBAQAOHWRAZkBnAEGBgAvk7ABjQQnAgIANIaiAb0D"
	.ascii	"hgEEBAAnh6IB7wK6AgICABl5kQGWAcUBBAQAU9vwAXuDAgICAEl7kgHCAqQC"
	.ascii	"AgIAi+72AdwE6QECBGwTYogAzQI7AgMZx6uBAKwEYQICADNykwHXAkACAgA0"
	.ascii	"X18BhQGtAQYGAEvR8AGCAYECBgYAKHOQAXmMAgQEACJqhAGVAZEBBAQAaej0"
	.ascii	"AYQB+AECAgBQd4sB8gG8AQICAFTG3AGNAbkCAgIAF2R8AbAE8wEFBQAELEEB"
	.ascii	"nAG9AQICADK61AHfAsACAgIAQcDYAfYCrwICAgBAqsYBvgN7AgIAI4qtAagC"
	.ascii	"vQIDAwBw5PYBEi0JCQAOTWwBjgG0AQMDAFXg+AHxAq0CAwMAF3GSAeUBwAEC"
	.ascii	"AgBIw9sBjgG9AgICADOEowGDAaICAgIAW8vkAY4BwwICAgAsg50BfYoCAgI3"
	.ascii	"d8vgAKYBwQECAgBL2OgBpgGdAQMDAEXF5AGbAYgBBgYAKpu7AdkCqwICAvQB"
	.ascii	"Zc7nAgMH7QvdAp0BrgEekAIsfpUCoQK0ARkZAMalWQHlBCshvgFWBxMiAJ8B"
	.ascii	"+gF7JOECK4emAK0BJBwcAAtHYgGpAkcbGwDQsmEB+wFVExMANZy3ARVvFRUA"
	.ascii	"DUhmAbUCAApPlAI4aXUCSn8eHgAHGyoBigS7AQcHAEO92wGHBMQBJQ7LAhli"
	.ascii	"gADTAz8bLEwig6MAkQM0EhIABCk9AbcDGxsbABZpiQHUAvsBFhYAEB0sAZoD"
	.ascii	"T00Q/QEVWncCFL8CUijGAQIVKAL7AokCaRWvAQohNgCAAsQBCQkAIVJkAc4C"
	.ascii	"iAEQEADcw2IBqQKRAQsLACtwhgHpAzEHBwAwosYBzwGRARkZADCUrgGpAg4O"
	.ascii	"DgALPV0BuQLHAWQCVEpNRgCVA64CHjGLAhA6VwDVAqIBBgYAUoyIAZoDXwUF"
	.ascii	"AE7L4gHeAY0BGh2WASNpgwLgAXEKCgAIJzwBaLcBBztcBx4zAJUBjQIGBgBN"
	.ascii	"tswBhwNlCQkAK4yiAZcB9gEEBABezOEBmQLdAQwMABNIZgH8AlUKCgATQFIB"
	.ascii	"aaoBCgoAQrrcAdQDLwUFAAs8VQHpA8cCFxcAEC5FAY4EABwFswEDDh4AdrAC"
	.ascii	"CwsAHGWIAdoDOgYGAEC21QGJAagCBwcAGGWEAaIEEgMDACx7pAF4rwEFBQAd"
	.ascii	"e5oBhgGLAgMDAF2xywHaAboBBAQAWdLhAdsBwQEDAwBXvdIBvgSbAhUVAAMJ"
	.ascii	"FgG2BBAMDAARO1YBS7UBDwNBHD5WANIEvwITEwADEiIB4wLAAQUFAM+cQQHH"
	.ascii	"ArkCAwMAD1BmAaQEIQIG9gEpdp8AwwHBAgICAGq+1gFQswEVAjs4gaUAvAQA"
	.ascii	"pwEFAAcTHwL+A64CCAgABQgNAeICpgICAgBWyd8BuAQfAgIAS4msAdsCtwIG"
	.ascii	"BgAtnrsBmQQjAgIANpa2AWG/AgICAC5ziQGKAbICAwMANKC/AZQEGAUKhgIG"
	.ascii	"RWEA6QQNDQ+HAgMTIwDJAs8CAwMAUczsAc4CrAIDAwATSmQB3gTmAQMDADCY"
	.ascii	"xwGtAaQBBQUAUJ21AaoEGQICADptjQGLBLsCCgoAAgkQAeQEFgICACVFXAGM"
	.ascii	"AbECCQSpAh1tkgLjBPYBAwMAI3SfAaEBygEEBAA6lLABoQGlAQQEAFLJ4AGa"
	.ascii	"AasBBAQANqvOAdQCsQICAgCF6/kBjwGDAQQEAD621wGwBCYEBAAXYnwB1AKk"
	.ascii	"AgICAA81RwHjBIkCBAQAGmKPAcMEIwICAC1piAFyxAEEBAAzja0BoAOsAgMD"
	.ascii	"ZDFNYwDAAcgCAgIATprBAaEBwgEDAwCY9foB0gK4AgICAHDp9wG2AcwCAgIA"
	.ascii	"S4OfAYUBjQEHBwAwpsMByALJAgMDADuwxQGYBCcCAgBLs9oBywKxAgMDABFV"
	.ascii	"bQGWBBcCAgBLrtMBrAQeAwMAEjlVAZIE9QEDAwAaWngB8gK1AgMDAE7S5QHg"
	.ascii	"BN8BAwMAD1qCAd0CoAICAgBTnK8BpQQaAgIALGaDAdsDGQMDAAxggwHMAs0C"
	.ascii	"BwNcIYOnAOMECBADCAoiMgDGA4MBAwMANqHDAZUDwwECAgB6uM8B3wKjAgIC"
	.ascii	"ABx8nwHPAj0CAgDEq4YBwwHFAgICAB1slAFqzAECAgApUmwB1QTaAhYbrgEH"
	.ascii	"IzsA1gMSBAIKNqXNAIgBqgEEBABV4foB+gK2AgMDAEB8lwHeAqoCAwMAIX2X"
	.ascii	"AZMBvwIDAwAhbowBzwLBAgUFAC+jvwGSAZIBAwMAd/b6AewE4wEGNIkCBTRU"
	.ascii	"AtcCqgICAgA7b3EBwgKmAgICAJPr9AGFAYECAgIAMYipAaMBvAECAgAwttEB"
	.ascii	"2gKoAgICACdslQHSAkACAgDHs3sBjwGmAQQEAF/o+wFnygECAgAvY34B5APd"
	.ascii	"AnVaqwEHFiUClAGzAQUKDlHa8wDNArYCAgIAQJuwAV21AhED/QEcWXUCkwHE"
	.ascii	"AQkC2gJe5/gAjgG7AgIC1gFSqMYCqQLnAQICvgEyVmwA1QI+AgJVKldZANQE"
	.ascii	"+AEEBAARVH8BpwGKAQQEAD/D4AFkwQICAgARUmkBdZICBAQAKmiFAQMI3A+X"
	.ascii	"A3sREQDTrVQBkAPzARMTACl4lQGnA9UBJSymASF8nQD5AyIHyQFJHkpcALAC"
	.ascii	"xwEREQDZvGgB0AHuASsrACuGowFpRyUlAAUZJwHEAbgChAEOciJngwK+AugB"
	.ascii	"CQkASz0uAfUDYRUVACiJqAGGAngVFQAujaYBA4wBJZACDQMPGwCvA3YFBQBS"
	.ascii	"wtMBsQNNDAwADDxVAcMBtAEQEABMu9IB2gI1CAgAKJO1AQMA/wIGtAEHJTkA"
	.ascii	"6gLkARUVACEyPgHqA4oCFRUAAxcsAeYBKi8IkAFDZWYC+AGnAT0HqAG5llAA"
	.ascii	"vwKFAQsLAOXXfQGsAmMUFADkyWYBxQMJBgYAKZe8AcoCLAoKABhWbwHNAoMB"
	.ascii	"HBNY2bBRAD2eASQGjgEgUmgCrQNhBQUATbXGAcYCmwEFBQBKkpIBH1IbGwAS"
	.ascii	"UW4B1gM1BRxhDEpmAOUCrQEFBQBBSlMBywNxCAgADERiAZYBW0QX5AIHKT0A"
	.ascii	"sAPBAgMDADqIpgHPAZwBBQUARcLbAaIDCgoKABNgfwG7A84CAwMAPYKhAZMD"
	.ascii	"yAIDAwA5eZkBvQLwARYkoQIGJz4C8wLGAQoKADw8PgHXAsACVgVbAx80AA6A"
	.ascii	"AQoKAAs/WwGNAvwBBQUAN63OAeIBigEKCgAnhqIBkQJCBAQA6N2NAc8DVAUF"
	.ascii	"ADiszQG/A4ACEheTAgQXKwCWA5YCFSpRDCI2ArACOwYGAOTLdwG5A24HBwAi"
	.ascii	"iKsB6gK3AQUFAGFTRgHXA2kGBgAul7EBwwMqCAgAHnubAeIBpgEFBQBZvNMB"
	.ascii	"sQM5BQUAGmODAY0C6gEKCgAaX4ABugItBQUASIWVAYIBrAIGBgATVXUBWbEB"
	.ascii	"NAjVATqjxgKQAjcGBgDfsVYBkwLSAQgIABdGXgF/7gEGTDMhaIUClAHzAQMD"
	.ascii	"AE/A3wHZAqIBBQUAOIWUAegDNgQEAEHC4wGfAiQFBQAtepQBc+MBFBQABSI3"
	.ascii	"AboBkQEPDwArmbQB2AGUAQQEADizzwGnA84CAgIARniaAXzCAgsLACV6mgHD"
	.ascii	"A2MFBQAIQV8BowGGAgICAHLG3QHFBMECBgYAByA4AZYBkQIDAwBw3+wBnwO5"
	.ascii	"AgMCtAFNeZkA/AJrCAgAKIukAVWoAQUFAD2jxgHnAbIBBwcAK5GtAbEDiwED"
	.ascii	"AwAzpMMBnwPHAg8hkAIJMEwAkgM1CgoAAx8vAYsDZQcHAC6YsAGrA4ABAgIA"
	.ascii	"WrvTAWubAQcHADKVsAH9AY0CAgIAZa/EAZsDDAIjmgEOSmQAjwT+ATwPlAED"
	.ascii	"EiUC+QGCAgICAG26zgGFAlQZAk9+mnwAjQQCFgi5AQIUIwLYAzUICZMCSMno"
	.ascii	"AKwCiwEEBAArW2sB5APcAisMsgIPLEQAjgS4AQQEAErE5QGkA78CAgIANGF9"
	.ascii	"AeME/AEHLaECBipDAqoEygIhRA0DBw8CuwPCAggIAA4sRQHbAzIDAwAXaYsB"
	.ascii	"rAQQBwcAEEFhAagEJAICADZ+rAHbAcIBAgIAfuLwAdQDGQMDAAtUbwHQAzIE"
	.ascii	"BAAEKUAB3QG1AQMDAETI5QGZA14DAwBo5/UBlwH4AQMDAGzW6AHjBMsCBAQA"
	.ascii	"CSpDAacDlAIIBdQCETBGAPsB8wEGAwMhaIMA1QQJCAgABhkpAZoEtgECFFQK"
	.ascii	"TGkAngLiAQICAC1jiQF0pQICAgAOTWsB7gNFAwMAK465Ab8ECgICAC5RbgF0"
	.ascii	"pQEEBAA+ttYBowPGAgICDjdohAL8AaQBAgIALYaYAZwBzAEEBAA8jq0BnQNa"
	.ascii	"AgIAObPPAd0CtgICAgBJw+EBkQGuAgICABdcggHZA14CAgA2mbwBiwG1AgIC"
	.ascii	"AE2v1AGfBAApArYBBQ8cAIQClgICAtkCEF99ALoDfg8DnAIQaogC1QSlAgoK"
	.ascii	"AAIKFAGvA34CAgAHW34BxQK9AgICABBXcgH9AfgBAgJrWLLHALcEHQICADNw"
	.ascii	"kgG5A7kCAgIALVNpAaIEEwICAD2SvAGqAYcCAgIAEWmRAb0EFAICACRTcAGi"
	.ascii	"BCYCAgAqe5wBzQMXBAQAEV14AaoDxgIEBAAJLEkB0QGmAQMDAEKEnQGnAoYB"
	.ascii	"AgIAKYqyAcEBywICAgA3cpMBmAQWAgIATLHYAcYByAIDAwA/hJ8BlAPCAQIC"
	.ascii	"AFWXsQFgwAEDAwBBhKYBmQL8AQICAB2AowFYvgECAgAmOlABhATBAgUFAAQS"
	.ascii	"IgHYArYCAgIAE4yjAaMB/QECAg2B2u4A2ATnAQYC8wEfcpwCqQQeAgIACitQ"
	.ascii	"AaQBzgECAgBMe5ABtAQhAwMAE0tnAacDwQECAgAVZ38BqAGqAQQEAEO71wGw"
	.ascii	"BCgCAgAid44BggGKAgICABt4kQGUA1kCBcwBNq7DAO8EAgQcjgIEChYAbLQC"
	.ascii	"AgIAKWyQAZ4BsAEDAwBBxOUB0gI8AgIASG52AcgCtgICAgAQT2YB6QQYBAQA"
	.ascii	"BR00AYECjAICAgBBibMB+wPBAgIC2QIyS1wC4QKxAgMDACGGqQHSArICAgIA"
	.ascii	"f+fxAcsCugICAgBDhqMB2wF8BgLUASxvhwDQArcCAgIAYNfqAWS8AgICAAxC"
	.ascii	"XQGzBBEDAkMFKEUAjgG+AgICIw1afwL8ArYCAgKHAhxOYgC4BBgCAgAXSWEB"
	.ascii	"2gTuAQcR0gIGNloClwNjAgJmI5y9AqABpQEDAwBX0+cB1gKpAgIFIj6FmwCo"
	.ascii	"AaMBAwMAUaO9Aa4EGwICABBAWAHwArQCAgIAY9n0AQMJ/RaQA5EBEhIA2rFT"
	.ascii	"AfYBwgIODgAKKUEBlgKRAlgHBRxVbwDTAZkCKCgALoyrAdMDyQEoKAAjh6cB"
	.ascii	"hASKAQ8PAAgoPgHFBGxCUowCBBAfAIoCawUFAG3c6gGUBAMMe7oCGWSEALEB"
	.ascii	"0gEHBwAnVmcBjgKlAgcHAAoySQHsAkAODgAebY0BmwLAAQwMANu/bwG4ARQU"
	.ascii	"FAAMS2YBsQKsARERAMiaRgHnATsLCwAFK0IBK/QBKysAAw0XAYMEaAYGAErA"
	.ascii	"2gGFA/IBBQUASbXTAcECzAENDQDgwWoBpQP3ARAQACaCogHyARYWFgAFHzMB"
	.ascii	"2gJtFBQA3LtfAWEANCLMAgQbKwCYAgAoGxcKOVUA5wNfBQUAQLzUAZ4DcQsL"
	.ascii	"ANOuVQHQAu0BHRtrEBclAAAoCB+0AQg3TACTAowBEREAJYKgAZID6gEFBQBA"
	.ascii	"psABVVcTEwAKFBgBiARIEyrVAh9xkQDSAdMBBAQATLfQAf4BQw0NADyfuAH1"
	.ascii	"AfIBBAQAVLzRAd8BrwEFKYQCLXKJAvQBYAwMADyiugEAhQE9S0oDEB0ArQJ2"
	.ascii	"Dg4A4NF2Ac8BtQEDAwC2+PkBhAPkAQMDAGW3xgG9AcwBAwMAJz1MAcwB4gEE"
	.ascii	"BABZvdUBxQGqAQUFAHjb5QGcAqUCBAQAO6fHAfkBjgEGBgAYQ1wB3AHoAQIC"
	.ascii	"AIji9AGGAiwDAwCsoGgBzAFZGBgAAiI3AY4CJAUFADt1jQG8AbsBCgoAPbjU"
	.ascii	"AYYBURISAAIdMgG9A0QLCwAILkUBBwAdPS0HLEACkQIxIReOAtapUwCAA8cB"
	.ascii	"CQkAEjNLAcYBzwEDAwBissgBmQKtAgMDADyv1AGSAXAKCgAJQmABoAO0Alkn"
	.ascii	"UhExSQI0LxAQAA9QbQGyA2IEBABPw94B+AK7AQQEALyNOAGWAmkDAwBciIQB"
	.ascii	"9QNXBAQANKzLAcwBvwEDAwB18PkBVYcBNwPFAh1YbwLrAz8EBAAHSWMBsQPE"
	.ascii	"AgICAEmivgH6AcQBDhZDGFZwAssCjQEJCQDm1XEB7gK9AQMDAFFDPQHEA0kV"
	.ascii	"BNECF2ODAtYCJAcHAApGZQHyAfoBBAQAJWWDAdoBggEEBABAsssB7AHsAQIC"
	.ascii	"AGzO5gGQAYECCAgAJHuYAfwB6AECAgBVts8B+ANNAwMAO6PGAbMDJg0NABhx"
	.ascii	"kwGNAuYBAgIATp6+Ab8C6QEEBAB6TiYB8gNfAwMADGB/Ad0DiQIPDwADFisB"
	.ascii	"lgLwAQgIABtfggHwA3QGBgApcIYBkgPKAgICTGCmyADNA1gDAwBOxN8BcqMB"
	.ascii	"DSePAjmrzwJqqwEGBgBMze0BTaoBAwMAK1pzAeMBqAEEBABwytsBrwHtAQMD"
	.ascii	"YGC30gKtA3cDAwBz4e4BkAL4AQ0DCzifvgLfAi0FBQAkjbEByAMLBQUAL6PK"
	.ascii	"AWh1Dw8AAiE3AcIBgAELCwAwip0B6AK1AQQEAE1KRQH3Aa8BAgIAjIyFAfcB"
	.ascii	"tQEEBAAmgJgB6wNsAgIAULzRAbQDdgcEowIUYYAAxgLjAQUFADg0MgGnA+UB"
	.ascii	"AgIAR6nGAQ9/GQXFAgcvRwCCAcIBBBeOAkd+lgDiA20GBgAmiKIBsgNsAgIA"
	.ascii	"PqnNAcgDaQUFAAtAYgG7A24EBAAsnMABXKgBBQUAQ7nbAb0C9QEFBQAJHjIB"
	.ascii	"6QH0AQICAEy3ygHOAyMHBwAbepsBjAPdAnJ/fAwrQwLPAZwBAwMAXN7zAcYB"
	.ascii	"ZQIcXixOVQKTAmQDAwAzfIYB+wLMAgk2AwUiMgCDBNwCAwKWAjdeegDPAjYE"
	.ascii	"BAAmcYUB0gHvAQICAFSvyQHYA2cCAgBVyeEBhAG5AgICAGe+0wG4AcoBAgIA"
	.ascii	"crzMAdACmAEDAwDNxV4BggG0AgMOigIYYXsCqQN7AgIAOnFuAX65AgICAE2e"
	.ascii	"uAGoA38CAgCYwacBqwOJAQQEABppgQHiAdUBAgIAUKXGAcgDKQICADajwQGT"
	.ascii	"AZACAwMAZdHkAYgD6QEDAwAsYYMBsANwAwMAE3mcAdsDTwMDAEa52gGTA4IC"
	.ascii	"AgJmYanFAI0D7wECAgAQSGYBiwPlAQIC9v8DaqfEAIsDhQICAsIBY4CTALkD"
	.ascii	"ywICAg9Oob8A2gHpAQIEkAIXZ4EAwwMtAwMALZa3AZICRgMDAO/lgQGIAt0B"
	.ascii	"BgYAG2yLAdsBuQECAgCJ8/wBe6sCBQUAFlR4AccCmwEDAwAtlKwBhQGyAgIC"
	.ascii	"AC6UtQGrBBMFAq0BKmF/AJID9wECAgA7mLkBoQTFAhERAAMECgHOA1MCAgBZ"
	.ascii	"1PQBwQKXAQQEAC+PogHTAboBAwMALZi1AYUD+gECAgAVX3sBzgGsAQQEADap"
	.ascii	"wwHfAzgFBQBCw+EB6AG2AQICAEa52AGmA9sCAgIAIUpqAfIDaQICAD+2zAFy"
	.ascii	"lwEKCgAyla4B1gKNAQICALqWQwGOAj4CAgDUxowB+QJtAwMALaK9Af0DbwIC"
	.ascii	"ABlkewHFBL8CAwMAEDdTAfsBhAICAgA2jKsBfskCAgIAQpi0AaQD2QEFDoQC"
	.ascii	"HoWmAKQB9QECA4kCFWB4AnHKAgQEAClujQG4A+0BAgIAC1d7AZEEBgYGAAIS"
	.ascii	"IgGBAZACAwMAF2CAAZQEuwEYBL8BEElhAN0CpwEDAwAqd5EBygGxAQICACKd"
	.ascii	"xAHtA1UCAgA4qssB4QKtAQICAClcbgHqAakBBA/PAiiGpwDQA2gCAgA6nLgB"
	.ascii	"xAHiAQQCggIOZYMA1AHMAQICAESduAG1AjACAgC0qIUB2gGVAQMDAEbF4AGI"
	.ascii	"A2gFBQAyn7cBhQLoAQQEACN0lQHhAY8BAwMAKZu2AasB5wECAgdNsc8A2wNp"
	.ascii	"AgIASrbJAcMB1AECAgATZoUBmgJ0AgIAUoCDAfwB7QEDAwAScJIBgQP6AQIC"
	.ascii	"AA1acgHMAegBAgIAFGaEAa0DvgIDAuEBSJi4ArcDjQEFBQAYcYkB0gNsBAMP"
	.ascii	"IoGUAsECMQICADtuawG9AjICAgCdrpkBugP+AQICADeUugHoAeABAgIPSa7P"
	.ascii	"AJMDEQ0CSxFRbQCQA9ECAwLKAkuHsQLIAecBAgIAF22IAeMBugEEBAAgi6gB"
	.ascii	"7ASBAgkkWQQnQwBgzgEPJg4CHjMAsAOOAQICAD6oywGOA/8BAgIrR6C+AFSh"
	.ascii	"AQICADZoewGLA/cBAgIAGWCEAYUBpgICAgAUUm0B8gNlAgIAFGuJAZcB8gED"
	.ascii	"AwBFr88B/gH6AQIFmgEbeJkApAO+AgIC2AFMeJEA+gNlAgIAD3mYAYQElwIl"
	.ascii	"DcUCAhQlAPID2gIEBAAROlUBrQSAAggIAAQYLwGjA8ICAgIABDBKAZQDwwEC"
	.ascii	"AgBurscBpgPMAgIC+QFfkbQAmAJvAgIAUJSSAa0DwgICAgAjZocBsQOVAgIC"
	.ascii	"ACE6TQF2pgICAgATTm4B3QMuBAQAFGWGAb4DiAECAgA1lq8BkgHxAQICACuU"
	.ascii	"tQGwAz0DAwAdaIcBswPpAQICAA1oiAGqA5YCBAK8ASRJYAKFAcYCAgKTAUqk"
	.ascii	"vALmArwBAgIAt5NcAdEE/gECFqUBBSc6AHn3AQcHAAUjOgG4BCMCAgAIQGAB"
	.ascii	"9wGAAgICzQGd5vIC3AKeAQICDFNrbgKoAZMBBAQAKZq5AbQDVQIGgAIZZHwC"
	.ascii	"9wNqAwMAJHSaAVmfAQICADdrfAGYA1kCAgAmoLgB+gPbAggGYAkdLgK/A4IB"
	.ascii	"AgIADFp6AcUDAwMDAB+CpQGsBAQEBAAFDx8BjgP0AQICADaBnwHHAd8BAgIA"
	.ascii	"EXWaAeIEkAIEJ7ECAxMiAs0CsAICBJ0BWKu1ArkBkQEEBAArpL4B1gM0AgI4"
	.ascii	"EnCOAqQEJQICAC+BpwH9AfYBAgIAHmV/Ad0ECQUFAAIRHQHfAq4CAgIAHXKT"
	.ascii	"AdgDGgICAAVSbwGpBAkCBmEaUHIAoAHNAQICAEWCmgHZBOQBAgJXJW+cAIwE"
	.ascii	"tQECAgBDtNQB2wQUBQUABSI1AawDfQICABRzkgHqAswBAgJWIStIAo4BrgIC"
	.ascii	"AgAgcZUBAwqMHuIB3QKiAQ2QAiaHpwDwA8MBBgYARMPdAdAD1QEHBwA/ttIB"
	.ascii	"ywMQUBJJFGKBAMYDgwGDAQ3eAgsrQQKuAbUCFBQAMpe3AaoDnAELCwAnVWIB"
	.ascii	"6AHOAhAQAAQkPAGsASYREQASVnMBiAODAQ8PAM6nUQGbApcCBwcAET1XAbgE"
	.ascii	"uAEJCQA0VWQBzwGAAgUFAE++0gH2AZACBAQAZdHjAdAEZw4OABFQcAGJArAB"
	.ascii	"DQ0AvKRkAfwC8gEFBQAjaoYBswGEAgYGAEi4zwGwA/cBBQUAQrfVAZ4DuQEP"
	.ascii	"MPsBGmOAAtEBpAIEBABVydsBqAHUAQUFAAsnOgGMAs8CDQ0ALHKPAfECDwOF"
	.ascii	"AbgBM2BpAtAEwwEODgADEiAB+AO8ARcidyF7nAK2BGYFBQAqjbABpgR1CkNg"
	.ascii	"BxAdAP4DrQENDQAYcJABgQK1AggIAA0nPQHuA7ABBAQARr3YAc0CtAEQEADH"
	.ascii	"mkUBuQPmAQQEAEW41gGFApsBCAgAHEtnAeYBmQIDAwByzd8BuARWBgYAJYGo"
	.ascii	"AfQBxAEEBAAeQ1MBtAKUAQgIAChoeAHOAlgWFgDVt2MBuAHPAQMDABQuOwGQ"
	.ascii	"AQgJNRQHM0oAgQI0BQUAP42jAfABmwEMDAAddZMB5wKdAQQEADhnbQGlAsUB"
	.ascii	"DQ0A38NsAfABggEGCa4BCSo/APYD5QEICAAfb5AB0gLPAQgIAOC7WwHQAbQB"
	.ascii	"BAQAovDzAacBlQINDQAjf6ABnwJTCgoA58ViAdEBugILCwAylLQBG4wCO1cN"
	.ascii	"AxUlAPQBSgYGAEW40wG8AY0CBgYAH3OZAbYB3QELCwAjepcB5ASsAScguwIH"
	.ascii	"LUYC+AFxDAwAMZKrAYcETgQEAC6YugH9AVsFBQBBwtwB+gKLAg4OAA0lOgGt"
	.ascii	"AgoKCgAPR2gBQ3oSEgAHFB8BqgInBgYAPHyQAesDtQECAgBi2fIByAM5BgYA"
	.ascii	"AiM1AbECfgkJAOndgQHrAYgCAwMAZr/QAb8DqAIGBgAiQloBsAPPAQICAG27"
	.ascii	"0QGKA74CM6kBPxFBXQAjSBcXABRVcwEKCgoKAAQXIgFGGg4OAA5AVwHXAvwB"
	.ascii	"EREABhUnAYUD9QEDAwBizeUBoQNrDgJqral1AMEBowICAgB3yt4B+QH0AQIC"
	.ascii	"AHbZ5gHDApYCAgIARpSyAdUCmwIFBQAQQlwBuANUAxfMARhrigDiAugBBQUA"
	.ascii	"QzMuAesDYAMDAF/Z8AGXApcBBAQANKfMAaQCcQQEAPHmlgHFAbkBBgYAMKXE"
	.ascii	"Ae8B1AEDAwBj2+0B1gGFAgMDAC1uhAHFAhcHGvEBCkFfALcBuwEEBABU0+sB"
	.ascii	"zAH2AQYEvwFDt9IC5wEUFBQAAh0xAWV/LgWZASJnfwKKBGkCAgBYv9kB5wNB"
	.ascii	"BAQACEZfAZcD6AEDAwBFrckBmAQvBQUADkdiAdsBpwEFBQA1jKsB3AOrAhsQ"
	.ascii	"8AEPKDoAyAO2AhULFxc+VgKvAbMBBgYAI46tAZMEZgUFACaJqwGdBG4CAgBh"
	.ascii	"qL8BsAI8BAQA8OOHAeQBQAsLAAUqQAG1A8kBAgIAWLfQAaoDgQIGBgAhbIsB"
	.ascii	"6wH6AQQEABdvhgGMAskBBAQAH0JQAeEEqQEGBgAEHjMBjgJ8DAwAH4ioAakC"
	.ascii	"YggIAPDYZgHEAbABAwMAfejzAdkB5AEDBUldv9QAxwGqAQMDAJ74+wG3A50C"
	.ascii	"BAQAGD1aAccBhwENEKMBK523ANYDRQQEAAk/XAE/C2sdkQIEFyYAjQISCwsA"
	.ascii	"AiM6AYoCbAQEAIju9AGtAcsBAwMAR5m0AQBGEybJAgxHZQKLAYACAgNhUavD"
	.ascii	"AJYD7gECAgAWXn8BmgGBAgcHAB90lQHiA7ABAgIAQ6/TAdIB1gECAgBz2uwB"
	.ascii	"9gH2AQICAHTS4AGzAQgnCUsHPloAGQJOB9wCCis9ANwClQIDBeYCEy06As4D"
	.ascii	"XFMCCCKCogLWAfMBAgJzgeD5Ao4ESAQEAAxPbQHHAdEBAgIAg+H1AeMDYQMD"
	.ascii	"AETF2wHnApgCAxyyARRliACBBGkFBQBLyOEB+AH6AQMDAChjgAG7AfABAwMA"
	.ascii	"IG2MAe8BlQIHAwEYZ4gCyAKLAQoKAOXWdgGtA80CbQQUDSpBAu8BVQUFAEmt"
	.ascii	"xwGhAn0CAgBoincB1wHHAQICACNFVgHoAbwCAgIAHz1RAZYCIwQEADB4kwH5"
	.ascii	"A3YFBQAycIUBsgN2AwMAYdnmAc8CngEEBABFkJ4B5QSNAQkJAAMWKgGQAc8B"
	.ascii	"BAQAOn6dAaYCggECAgB5nX8BvgHqAQICAF3a5gHwA1cCAgBItNcB5wOrAQIC"
	.ascii	"AFC20wHEA1AFBQAZWXUB2wPHAgICowFJaYUA2ANuBQKfAjaJpAB8vgEHBwA/"
	.ascii	"sdMBzAHjAQMDAHDW6QGUAYoCBAQAOqjEAYMCjgEDAwBEl7UBTa8BAwMAHzhL"
	.ascii	"AdoCNAYGAC6gwgGnA+oBAgIAD1F4AawCogEDAwDmulEBkwRYAgIAOpu8AWC1"
	.ascii	"AQcHADmRugGOAu0BBgYAGVd3AZsCZwQEANnBZAGEAioCAgChnHABjwMAPxtH"
	.ascii	"FWeGAvECngIEBAAicZABtAP/AQQEAC+auAHKApsCAwMADFNyAcgB9AECAgBR"
	.ascii	"p8IBqgFiAiWFAjFVYACNAi4FBQDAllMBugGbAQQShwJQobcCBXoHF7oCBytB"
	.ascii	"AqEEcAMDACFVbAGDA+EBAgbJAXXI1wCeBGoCAgAxj64B6QG1AgICAFKu0gGk"
	.ascii	"ApUBAw/4AcGbVALiAaYBAwONApHt+QCLAkECAgBdm5cB+QGMAQMDAA0pPwFK"
	.ascii	"lQEZBpsBGj5PArEDuwECAgASZoIB3gO+AQICAD+wyQEMHhkC1wIKOlQAwAGb"
	.ascii	"AgICAFOcwgHAAsQBAwMA69uDAbgDsgIFBQAOHjABlAF5IQMBNoukAqgCSgIC"
	.ascii	"ALiQPQGEAtIBBQJqVKXHAvYBugECAgA2r9ABiwHBAQQEACiSsQGSAvcBAgRR"
	.ascii	"TsvmAJAD7QECAgBYxNYBngJ3AgIAy8OAAYgBjAEEHo0CI4inALwDcQICAEi5"
	.ascii	"3wGTAuIBBgYAEFFyAaoDLxEJ1wIVYoEAsQPLAQICAA1ohQGnAkAGBgDKnU8B"
	.ascii	"zAJ4AgIAyKIuAeECHgIMXBNWdgDuAbMCAwOgAT+OqwD1AbMCAgIAPHufAc8E"
	.ascii	"eAICABgpQgGEAbYCBQPVAmfJ4ACYAuoBAgIAOHifAbEDygIEBAAHLUcByAML"
	.ascii	"AwMAOrjgAegDdAQEACpthgHPAjkCAgAoWmgBlQJDAgIA9O99AdkDuAEEA4UB"
	.ascii	"DWiJArgDdgMDAAxYdAGTBG8FAg5HiKIC2gKjAQMDACGDqQFjqAEFBQBKyekB"
	.ascii	"5ANtAgIAQaa/AYYCRwUFADOmxQHFApcBAgIAQ4h5AZYCAQYGAAgwSwHZAYIB"
	.ascii	"AgIAUtHoAecDsAEDAwAOcZIBkwPJAgICAFumxgGzA94BAgIAPZy8Ac4DHgMD"
	.ascii	"ACWHqQGRAfgBAgIAF1pwAeMBogEDAwBFwt0BxAGxAgIDCw9ngwDsAZICBAKc"
	.ascii	"AhxhhwLXAcsBAgIATJqyAa0DhQEEBAASco0B+ANOAgIATLzgAYoD7AECAgAT"
	.ascii	"VXEBwQOaAgcHABIoPgGzAewBAgIAIXOMAcwCMQYGABpgdgHuAYsCAwIGG26I"
	.ascii	"AOEBrgEDAwA4kaUB8gGlAgIClQFHs80AigRXAwMADWGCAesDbwYC2AEpe5QA"
	.ascii	"swFmCwsAAiM3AZMD0wICAgBblbwBgAP8AQICAC5viAHoAfMBAgLMAn7n9ALO"
	.ascii	"A6YCAwMAESQ0AaACLAICAM65YAFPqQECAgAzgKEB+AGvAQICAKydfQHuAfIB"
	.ascii	"BAQAGHWWAeQDNgUFAD3A3gGoA3MCA+YCS39/ArsDagICADumxgGWAvUBAgIA"
	.ascii	"I3eaAe8BrwICAkROqcYCqgTSAhsSVQMDCADxAr8BAgIAKS0mAa0DvgEDAwAi"
	.ascii	"kK8BiQNsAgLDAT6BeQK/AzADAwAsh6UBmAKmAgICABlqiAHXA84CAgJULEpl"
	.ascii	"Am/EAgUFAB1tjgG8A84CAgIAV6TDAacDfwICwwJVj4QC+gLaAgMDAA0bLgG2"
	.ascii	"A+sBAgIAD16DAXylAgICAHDI3wGTAfsBAgIAG2F+AfABtQEFBQAdg6UB2wM7"
	.ascii	"BAQA"
	.ascii	"TtHvAfQB7wECAgBLqMUBfrUCAwMAEmF+AbEDiwECAgBEvdwBtwOJAQICAAxX"
	.ascii	"dQGRBHECAgARXHQBtQPTAgICABg8VwH3AcoBAgIAM4mnAaoEEgICAAopTQGT"
	.ascii	"AmoDAwAmgKQB2wNPAgIAWtLwAbADwgIDAwBClbMBzgHMAQICAD2aqAF1sQIF"
	.ascii	"BQAYaZEB8AGIAgICACh6mQGIA8MBAgKjAjhohADvA2YCA3U3pr4AhAP6AQIC"
	.ascii	"ABRgeQG7A+0BAgIACVx/AdICNwICACCKqAHbA9ECAgKSATNNaAKrA84BAgL9"
	.ascii	"AR9rhQDSAe0BAgLCAm/J3wCCA24EBAAkh6EBmgH0AQICAFC4zgHoAaoBAgIA"
	.ascii	"XaK5AZgCRQICAMSmPQGrBBcCAgAsXn8BtwNuAgIAEnydAYoDZwQEADCkwQGJ"
	.ascii	"A/UBAgdWHWSIAIcD6gECAgAdUXoBhwG8AgICABhecwHGAyoCAgAxoLwB4AKq"
	.ascii	"AQICABhafAH5A24CAgA3la4BkwJhAgIAOn6KAe8CvAECAgBWPCkBwwMNBAhk"
	.ascii	"IHyhApoCKwICAMKwcAGFAYoCAgIAXLfRAdMDZwICABSDowGiBJsCJBKXAgMH"
	.ascii	"FACLAuUBAgK8Amm72wC9A4YBAgIAG4WeAXKSAQYGADmargGKBAACB8ABBSY8"
	.ascii	"ANkBugECAgB66fYBiwPtAQICHwU+WQBxpwEEBABHxecBzAMPAgIAGXyiAYwE"
	.ascii	"UwICACWApQHsAmkCAgDhxnoBgQLoAQMDAB5yjgF9yAICAtYBZbjRAJgD8QEC"
	.ascii	"AgAyjagBpgJ4AgIA3b5hAZQC7AECAuMBNnObAu0B7AECAgB11e0BzwNTAgIA"
	.ascii	"XNj4AWiMAQICAB5BUQHaAcMBAgI8eMblAo4D9QECAgA5h6UB1wMxCQKWASF/"
	.ascii	"nwKbA/QBAgLXAgpmhwClA+UBAgL0AWO52ADoA7IBAgLsAUa11QLzA3kCAgA3"
	.ascii	"Z34BrwGYAQQEADa51AGQAvYBAgIAGH2fAYMBxQICCFQcbogCtwHGAQIE7AFt"
	.ascii	"vs4CswNuAgIAPKTMAZACQwMDAOfdkwH6As0CBQJ/DDRLAAML1SO1ApkCBAQA"
	.ascii	"Z9DjAWXVApcBEbkBCS9IAOUDFwQEADiqywGmAo8CCQkAET9cAYsCuQEICADQ"
	.ascii	"uXoBgwQqBAQAOqXGAYUEOTEIBSFujADgAp8BA3mOAhs/UwCaA4sBCgoA6cFc"
	.ascii	"AZMCngIFBQAMMEkBtgKoAgUFAD2y0QHPAgIrFQoDHC8AugSWARUVAAULFgGf"
	.ascii	"AbkCBgYAQLnSAaMDpgEKCgAoS1gB+gOIARE2aBtbcwKDBNMBBAQAP7PZAb0B"
	.ascii	"swIEBABUzOoB6gPGAQQEAFPP6AHhAwkICAAMVHMBwAOsARERACmJpQHXA+gB"
	.ascii	"Dw8AH36gAZACiQINDQAoepwBhAS+AQQEAErI5wH3A9sBBQUALZ/IAccCXhQU"
	.ascii	"AOC+YAHzAlsJCQAfRlgB9AO8AQUJkQJNy+gAsgGIAgQEAF3P2wGLApIBBQUA"
	.ascii	"L5u7Ae8DFSQLmAEOUG8A4AJ5Dw8A471bAfwBgQEFBQBArMYBugTVARAQAAQd"
	.ascii	"MQHkAogCCwVxPywsAKcDkgEEBAAyXmsBrwHTAUYJuwEee5sCiAKrAgUFAAsm"
	.ascii	"NwHvBBIEqwGXAhNNawDbA4QBEBAABjVTAbEBpQIDAwBw0uQBkwKpAQoKAL+W"
	.ascii	"TwHtAYABBQUADSw/Ae4BsgECIocCGkpcApEBngILCwAcdJkBswHQAQMDABEo"
	.ascii	"MgFN+AEfIgoEGy4AF/4BFxcABQoPAcACPwoKANapUwGOATsjCSgIP1sA1AKz"
	.ascii	"AQwMAMiYQQGuAjAFBQDGrX4BjgRtCByaAh1JXwL7A6wBAwMAM6fFAfMBkQIE"
	.ascii	"BABcx9wB1AL9AQUnjAIbSF0CtgG9AgICAHTE3QGTA5kCEhIACB0xAbcChwED"
	.ascii	"AwDz8r0B1QGkAgICAHDh8AHzAjAJCQATVXQB4wJeBwcAxq50AdwD8AEgApoB"
	.ascii	"GUhgAOoClgEEBABacl4B6wO8AQUFABVylwG3AhkKCgAFLEcBzgKRAgwGzQEj"
	.ascii	"Z4cCmwPTAQICAEiJpwHpAWkLBIECSam/ANoBsgILCwAzmbYBxAR2BQUADCg9"
	.ascii	"AccBhQIZBAYpe5UCtAKmAgIQjQILXn0AzwRwAwMALnqgAccDlAEGBgAXNUsB"
	.ascii	"jwN0JAhd3bVZArcCwwICAgBGw+IBrAKWAQUFACJUaQGPArkCCAgAI2mIAZ0E"
	.ascii	"rAECLosCFWB/ANwB/wEGBgAed5gBzQGlAgMDAEzF2AGdBMwBBwcAHHCSAeUC"
	.ascii	"oQEFBQA3WmUB8wMLCQkADFNyAbcB1QKTAZkBrgEaV3MC+QHAAgoKAAQeNQG/"
	.ascii	"AsYCBAQAHWF/Af8D4wEFBQAicJUB7gOzAQMDAFrX7gHHAcIBBAQAWM7kAeIB"
	.ascii	"mgEDAwBBudQB6QGMAQUFABtxjgG2A84BBAQAEGN/Af8BlQEFBQAVOVUByQGz"
	.ascii	"AgICAGjB0gG6A+8BAilKGFBqAp4CoAIEBAAwmbcBQgYEeMkBCy0/AKMDggID"
	.ascii	"AwA4nb0BkALDAQ0EqwHbwYQA6wGKAgICAJDm8AHWBL8BAinLAQkwSQC4Ap4C"
	.ascii	"GgIJIHqcAM0CRgQEAOnWfAH+AusBBQUAI1VyAboCAwYGAA0/XQGIAXQICAAI"
	.ascii	"QmEB6AGjAggIADCVtgGBARU5Bq0CCzxTAJgD4wEDAwAPWXcBkgEKCgoAAhYo"
	.ascii	"ARlYCQkAF159AdABxQIDAwBJh6YBWzwPDwAEEx0B+wN1AjeHAgUjOgCfAssB"
	.ascii	"BQUA2cGDAYgD8gEDAwBTzOcB1gPcAggGWiRkiQDRAf8BBAPOAmHJ4ADrATgW"
	.ascii	"ArQCJmqCAOwB0QEDAwBEt9cBuAP4AQQEABdqiQH9AvYBBAQAJm6IAaIEXgQV"
	.ascii	"lQEZUnAAhwQrWgQCD0lpApoChwENDgcce58AgAK6AQICAExzegG7A+YBAwMA"
	.ascii	"VdPuAYgESgMDADGStQHyAaQBAwMAKpS1AaAB1gEFBQAFIjQBsQKNAQMDADiC"
	.ascii	"nwGABFMGBgAYdJcB7gOsAQICAEHB3AHgAkwCAgBmeVsB5gFHAh8DHUVXAPcB"
	.ascii	"hwECAgASLTcBCAAVJR0FITEC1wKfAgQEABY3RwHyA5ACFhYAAhUpAe4DMQQE"
	.ascii	"ADGkyQFJZgsLAA0UFwGNAYACIQJYGXCVALUDyAECAgBnyeMBowLRAQICAMaz"
	.ascii	"kQG8A6ICAgIAMk9sAUEfCQkAEkhhAdEDRgM0bR9+nAD/ATsGBgBDpL4BvQKT"
	.ascii	"AgUFABZkgAHxAzsFBQARV3cBE2kJCQAQU3UB9QF5BAQAQ6G+AfACiAECAgAg"
	.ascii	"U2gBwQRtAwMAJ3aUAfoBqwECAx6spHwC5QOiAQgIACB6mwGtA2cCAgAuYHIB"
	.ascii	"pwGjAgICAEmvzAHzA6IBBQUAElp3Af0BWwMDAFPb8wGaAlkDAwDu0oAB+wNe"
	.ascii	"AgIAR6jHAbAD9AEDAwBExuAB0gKnAiUDViaFowKnASsODgASV3QB9QNbAgIA"
	.ascii	"TbvXAVawAQUFADl8oQHhAuYBAgIAa01LAc0BfwkJACyJoAHTAY4BAwMAOq7M"
	.ascii	"AeoDBQICAC6IqAGgAk4CBLIB8umZANMB9QEDAwAcepoBwwG0AQMDAE/R5QG0"
	.ascii	"AWECKooCQHqGAq4CuwIDAwAYdpIBLzgJCQATWnsBngIAEgwCEUprAP4BUgUF"
	.ascii	"ACiRrAHJAosBAwMA7tqcAYUD5gECAgCC3eoB9gNgAwMAEmOBAaoBgAIFBQAg"
	.ascii	"g6EBkwRJAgIANoeoAb8DxAICAgApTl4BkwKbAQMDACtwiwGEAi8CAgBLf4QB"
	.ascii	"mgGPAgICAG3Q5AGQBFwEBAAOZ4MBqwKXAQMMX7uRSgL2A38FBQAINE4BvQKU"
	.ascii	"AQMDACx5jwHOA0IHBwALRGABvAOqAgIDczdkggK6BGgEBAAnjLMBnAGyAgIC"
	.ascii	"AD6t0wGwA9MBAgIAB0leAZQCTAQEANGpVAGTA/EBAwMAF119AaoBtwICAgBP"
	.ascii	"ttQBywO7AgICADJddwHBAz4HBwADIzgB/wNbBQeTAhV2lgKZA+wBAgIAFmGH"
	.ascii	"AacD8gEGBgAnjrEBxgHPAQICAHfN4gGbAmEDAwDYsk8BqQJ8AgIA9+GwAYIE"
	.ascii	"PAICADiAnwGmAiYEBAArgp4B+AGoAQQEABtgfQGRAt0BBCaFAhpYdwLZAtIB"
	.ascii	"AwI6sp91ANIB0wEDAwBez+cBrQG6AgICygFcxdoAmgGSAgICTQ5XdgC8AawB"
	.ascii	"BgYAQLXQAb8CjgEDAwDq5JgBugNjAwMAB1l7AeUBmQICAgCM6PgB+QN0AgIA"
	.ascii	"R4OXAeoDswICAhw6T10AjARrAgIAI26LAboEtgELBGA5ODYCrQO3AgcHABE0"
	.ascii	"UgHpBM0BBwcADEJkAa0BWgIyVSE+SAKIBGoCAgBq2fABsQMXBgYAGHSVAbcC"
	.ascii	"jwECA4sBE0ZAAn61AQMDACGQswG2AcwBAgLUAhQoNQK7AboCAgIAEnaTAZ0C"
	.ascii	"SAQEAOu+UwHQAbQBAwMAvfn4AYUEMgQEAAtVcAGXAf4BAwMAFmF+AdMCoAED"
	.ascii	"AwAvj6UBpwGyAQQEACOYtgH1AZcCAgIAE2iIAaEEcAICL06BlwKsAb8CAwMW"
	.ascii	"ZLXLAuABkwEYA+YCHnuYAtcCRAICAMK2iQHTAaACAgIATLHRAXnJAQUFADuP"
	.ascii	"rAGKAmsCAgC0+/wB4wNVCAgAIIOoAc4BoAICAgAedpQBtQLJAgMDACyZvwHL"
	.ascii	"Ab8CAgIAUKrJAQE4CR4gDEViAJoCmgECAgBPrskB9gFGBAQASMDaAbkBuAED"
	.ascii	"AwBa2/IBfaEBBQUAKIakAcsB3wECAgA/qsoBlAPpAQMDAEvA2QGpA/oBAgIA"
	.ascii	"DWKEAdsB6AECAgCD4PEBkAKJAQUFABZ5mAHxAYICAgIAmtvpAYECogEEBAAl"
	.ascii	"WnkBnwGiAgMDABp0lwFkjwEDAwAfPEoB7wNcAgIACWGFAboBvwICAgAfg6AB"
	.ascii	"tgSuAQgC4QE0OUMCuQKNAQICAMjCgwGuAZgCAgIAEWGKAcUC/wEICAACHjUB"
	.ascii	"sQHLAQICAEeUqAGTAi4EBADIk0gBiATQAQYLACiHpgDLA1YCA1Jb0uwCpAF9"
	.ascii	"EAo+L5OuAsgBtAECAgAfn7gB5QPdAgMC1gExX4EAgAF7Aw7uATmLngLMAp0B"
	.ascii	"AgIAMpS/AXW8AQUFAECz1wGuAoYBAgIA3N6XAecDYwICAFfX7QHKA9QCCgoA"
	.ascii	"ByxHAYYCKwICAMywbQHNA7MCAwKzATtYbQC6A7QCCwciDyk+ALICPQMDAPPw"
	.ascii	"lwHEApkCAgIAEFp2AdoBxwECAgAjR10BggP/AQICADhoiQHUAccBAgIAIVlj"
	.ascii	"AdUCwwECAgDAji4BtQOuAgQEAAkXJQGkA+kBAgIAEWGFAaECdwMDAOHNdgGN"
	.ascii	"AYECAgIAXbbRAcsB/wECAgBZvdgB9wH2AQIGjAIYTmoAlAH1AQMDAFbE3QGf"
	.ascii	"AnwCAgBOfHoBvwHyAQICAD2TsQHWAawBBAQAN6jLAbEEYwMDACF4lwGkAn4C"
	.ascii	"AgDKypUB2gGfAQYGACSOqgG2BGQCAgA/qswBhwKiAQICACtFTwH3A3cCAgAh"
	.ascii	"Xm8B3gKXAgICAAklNAGxA7kBAgRWCVl0AN0DtgEDAwAZbpMB6ASaAQgtLAMa"
	.ascii	"LAKxA5wCBAIYFzxWALMCfQYGAPLiegHmAb0CAgIAF0BWAcwDNQMDAAEZMAFQ"
	.ascii	"rgECAgA2aYgBsgMoCAgAGnaZAcIBpgECAgBQmbgBrwG8AQQEAC+mwwG7Ai0D"
	.ascii	"AwA5jKYBfaoCBAQAF1NzAbkBxgICAgA7obwByAGpAQMDAJXz+QGiAYMCAgIA"
	.ascii	"N5e2AfQB9AECAgBi0OIBpgJXAgIA7s2FAbcDpwICAp0BL1BmAPwDcQICADR+"
	.ascii	"kQG9AsABAgJg69aeAq4DdwMDAHjt+AHoAfYBAgLMAgtoegKXAlIDAwDrtEkB"
	.ascii	"6QG5AgICAEN3kQH0A70CAgL0ASlGWACrAoMBAgIA6eeXAcEDpQICAgAtUnQB"
	.ascii	"xAO7AgIOEwgkOwCPAbwBAwMAMKLBAZUBiQICAgBNvt0B+QO5AQQEABl1mgGw"
	.ascii	"A2IDAwBf2/ABnARtAgKOAYO/1AKUBG8CAnUgXngCggG0AgICACKIpwGpAqAB"
	.ascii	"AgIA47FIAQ6NAQQEAAkoOwG3AzcEBAAVVnEBpgJzAwMA+fObAZAB0AECAgBS"
	.ascii	"jasBywRrAwMAHV19Ac0DogICAgAoQVABzAPIAgICAB09VQF5xAIGBgAhfZ8B"
	.ascii	"gARiAgKLAkzK5ACqA4ABAgIAZb7OAbIDaAICABBulgG8A8ICAgIAHTtVAbgB"
	.ascii	"fAUFAC96jAF2yAECE2QaM0MCqwP9AQICAAtVeAGfBGsCAgA9m7cB+gM3AgIA"
	.ascii	"IniXAfQCngICAgA8fJgB3ANFAwMABjxWAccB8wECAiCB2O0CrQI6AgIA7c9v"
	.ascii	"AbMBmQICAgAzkKwBmgIlAwMAMXybAfYB8QECAgBe1OQBuwMSBAQAEF16AYwC"
	.ascii	"PwICmAHAyJgAtQGDAgICAC61yAHjAaQBAwMAUc/mAa4DiQECApACQrPTANYB"
	.ascii	"zgECAgAhiKABgAG4AgICAD2SqgGOBGgCAgANZoEBogJWAgIAz7ZaAYYBiwIC"
	.ascii	"AgB+0+sBqgJMAgIAvZE5AeQBqQECAgCg7/kB3QJKAgIAub2FAYoC5gECAgAh"
	.ascii	"eZgB1ARzAgIAH1l+Ae8EeAYuXAMZLwCTAnwCBK4CGpq4ALkDhgECAvUBOpWv"
	.ascii	"AP0DagICADetyAGoA+oBAgIADlF3AY4E1wIXG5ECAhIgAGuqAQUFAE7S8gFZ"
	.ascii	"uwEFAo0CQ3SUAPADsgICAqgCK0dUAtMBlgEDAwAgj64BiwJDAgIAS5edAYcB"
	.ascii	"uAICAgB53fMB7gH2AQICADWOrgGGA/cBAgLmAQVAZALEAZoBCwJdMaPCAOcB"
	.ascii	"qgEFAmc3iqUAzQHkAQICAIbn9QGXBG8CAnhXjqQAygJ3AgIAy7E7AfMDtQEC"
	.ascii	"AgARc5QB9ANzAgKQAT6DlgDvAf0BAgIAJ2mIAasEGQICAD5vkAG5AaIBBAQs"
	.ascii	"RpCtAs0BywECAo0BXL7NAvQD5AEDAwAWX4QBjgP4AQICABpjhgGvA84BAgK3"
	.ascii	"AYfW6wC3A2cCAgAGV38BkQLtAQIC8wFFdJQC7gGxAgICACV8mgFzhQECCDQ9"
	.ascii	"eYcAlgLoAQICPEKFqwDNAqMBAgIApqR+AeMEqAEFBQAEITcBsQPDAgICAEuq"
	.ascii	"yAHAAsUBAwMA8OKBAQMMzSbWAt8BCAgAPDQxAcwDvQEODgApk7QBgQOaARQU"
	.ascii	"ANKrUgHoAtoBCgoACzNPAaMBxgIKCgA0iaoB3QPAARsS0QEbe50CjwQ5CAgA"
	.ascii	"J4CeAa8C3QEGBgArW2sBes4CHyeOAgs/XACbA7ABCAgAIEZZAcgBzQIwS7kB"
	.ascii	"AiA3AO8CSgM85AI2YGkAngLsAQQkPB5hgQDQA58BCAgAK3eTAYIDHA8PAAUv"
	.ascii	"RAGeBK4BEAveAjtHRgDHBEIREQAWXn8BoARcAgIATZSwAe0BvQJbBHEicY8A"
	.ascii	"xQReCwsAEld6AY0D3AEJCQAeUWoBAJkCpQEPWwIVKADFAnQDAwDs36EB0gN5"
	.ascii	"CgoACz5bAcUCAEwKsAEDHS8A9QGbAhENJSx7mgCOAp4BAwMAKk1aAacDqgED"
	.ascii	"AwA3boYBjwN6DAwA0KVLAekBfAUFAAknOwGVBGUFKZACHEheAN4DHRAJqgEQ"
	.ascii	"YX8AtAGOAgMDABtkhAHQA9YBBQUAT8/rAZ8EPQICAE6dtwH8AbABCQUJ1bpv"
	.ascii	"ALEChQILCwAJNVMBpAPOAQMQ/AETTGUCiwK3AQUFAOLNjgGuAdEBAwMAESs3"
	.ascii	"AXzYAWQCkwEsfpgCiAK6AV8CF86oVACJAUJWFL4CBjJMAsADsQECAgBly98B"
	.ascii	"owOhAQYGABo1QQHfBGcSCAkPU3EA/gHCAQYGABE+VwGNAoACBAQAL5zBAbQC"
	.ascii	"aQMDAPTqngG+Ak8DAwDt2ZIBxQOrAQICAFiwyAGfApUCBQUACCpDAb8CqQEM"
	.ascii	"DADCk0UB4AKVAQcHAMqhSQGzApYCAwMARb/YAZACrAIGB9oCLIapAIcClAIC"
	.ascii	"AgBxv9UBtAO1AQMDADqrwAGzAkUFBQDBmk8B2AGhAgMDAEi60AHNAlgRBbgB"
	.ascii	"yqpbAr0DpAEEA58CUai9AKYBuQICAgBg2PEB+wHdAo0BGM8CKH6dAtwCcRAQ"
	.ascii	"AObAXAGZAbwCAgIAU8rjAb0DxwEEFI4CDmJ/AKQChgICAgBLhqMBuwG0AgQE"
	.ascii	"AFPF5QHrApEBAgIATGxgAfoDoQEJArQBLJGrAJUEBAIUWQ1AXwJwnQIHBwAl"
	.ascii	"Y38B6QKPAgMDAGU+OwGMArUCAwMAM4emAbYEvgEEBAAmZoMBkQKSAQQEACue"
	.ascii	"wgEaiAE/G40CAxAcAOsBlwETCQgXZIUAkgOtAncDzwEPKj8CqwGoAjICASp/"
	.ascii	"ngLWAlADAwDhyI4BjwLAAQUFANS5bwGFAqsBBQUAx5hEAbsC3AENAhMwWGkA"
	.ascii	"5QMZAwMASsLjAbUEWQQEACuGrgGsBJgBRwuaAgMLGACkAbECBgYAJpO0Ae4B"
	.ascii	"wwEDAwAgTV8BlQShAQYGACVOWwGEBCUDAwAphq8BuQHbAQICAFyjvgG6A+0B"
	.ascii	"Fg1nJIGkALcCqAIDAwBP0O8BnQPfAQICAESHnQGCAY4CFgNXG22OALkEdAcH"
	.ascii	"AA4oQQH7A4cBBBePAgUaLADwA8UBAwMAWub7Ae4DggEEBAAMTnABqQTGAQUF"
	.ascii	"ACJxjwHbAa4CAgIAYsDUAfABywEFBQAlfJYBoAKXAQQEABl0kwG8A9wBGgQG"
	.ascii	"Em+QAusBdS8ClgIql7UA5QFeCAKlAkRwgAIuWwoKABlOZAH0AwECAgAoha4B"
	.ascii	"2wFpDQ0ABSQ4AasE0gEFBQAFHzYBsQIpBAQAP3iIAYwE3wE/DAIDGzAC1QHe"
	.ascii	"AQcHAB18mgGbAqACAgsMRbXWAK0CMgQEAOO5fAGJArkCAgIASYilAY0ELgIC"
	.ascii	"ACp6oQHDA1cGBgAVaowB1gKUAgMDACd1kQGEAhhqA+YCBClDAJ0EYgUFABZf"
	.ascii	"fwG1ApsCAgIAlPH8AYUD7gEDAwA6pccBnAQ6AgIARo+lAdIEawQEAAlEXAHA"
	.ascii	"ArMCAiXt/wMfaYUA1QJYAwMA9Nd0AckB1wEFBQAdd5cB2QGmAgICAB5kgwHQ"
	.ascii	"AYECAwMAYd/qAbsEKwICADVmhwH8A9oBAwMAN6rUAb4CgwEGBgDx43YBiAS/"
	.ascii	"AQQEAE3S7gG/A5gBBAQAGDtSAeIC0wJ6FpgCCzBLAt4BSxsCogIkY3sChQTR"
	.ascii	"AQMDAEK93gGeA4QCAwMAMYqiAdEBhwICAgAJVGMBugLSAgQEADGMswHSAwwc"
	.ascii	"Al4NWXUAyQKRAgYGABNOaAGLAi8DAwDJkDsBzQJBAgIA8NKdAaYDmwIGEpgC"
	.ascii	"CRYpAL0CZwYGAOO9SwGoA2YDAwC+v3wB9gOXAQICADZ1gwGVBM0BBQUAIYOo"
	.ascii	"AcoBiQEEBAAzrMEBsQI6DwNUxJhJAuACoQECAgA7RkYByAHBAQMDAGrj9AGG"
	.ascii	"ApoBBQUAETtXAYsBKg8pvwIDKD8CpwOOAQICACZZYgG2AYgCAgIAeN/vAa4C"
	.ascii	"mgECAgAjR0wB/wG5AggIAAogNgH/AucBAgIARm19Af0C9QECAgA6iqgBxQI2"
	.ascii	"AgIAva1mAYQErgEICAAWaIkB9wNYAwMAQ8XgAbMClQEFBQAUY4MBgwP1AQMD"
	.ascii	"AFi/1wHeA6YCCAgAEis7AewBoAICAgBMscoBnQNmAgIAiKyUAcEBvAEFBQAr"
	.ascii	"pMMB4gGiAgICAFazygHoAV4LA4sCTbPPAN4ChQIKCgAGECIBBB8GBgAGHS4B"
	.ascii	"9wHOAQQThQIdc5ECswEeDQ0AEld1AeICXgICAOvXkwHGA4oBWASyAQYtRwD1"
	.ascii	"AZICAwMAdePwAfQDwQEDBJ0CWNfxAI4BqQIDAwATVXAB6QKZAQMDADNmZgH0"
	.ascii	"AeYBBgYAGX2cAaUBjgIHBwAhg6cBlAKiAgMDAAQjQAHVAe4BGQZqJomqAMAD"
	.ascii	"ggIDAwAXPlUBUFgLCwAQEhIBrAKPAQQEABtVbAG/AqwCBAQAFWqLAZ0BkAIC"
	.ascii	"AgAjdJEB2gKbAgIFKDtaaQD5ASkICAAGLEIBmwJcAwMA8d6EAc8CTgQEAMym"
	.ascii	"TQGqA2UCDakBIV5uAvMBcwQEAD+ovwGQBMQBAwMABE1sAZQErwEDAwAdbYoB"
	.ascii	"gARNAwMAC1d2AVUMCAgADTNHAa4D9gEDB6sBTcXlApoEEQMbpwENSWsCpQOH"
	.ascii	"AQICAMm5cwHsAdUBAgIAaNzxAY8EJAYEeAdNaQDjAqYBAwMAP0RPAdYDBwcH"
	.ascii	"ABNkhgHEAp8CCAXeASaEowAvHgsLAA1CWwGVA+MBAgIAB1BsAfoDrQECAgBG"
	.ascii	"w94BvwGfAgMDACR9mwGTAo8CAgIANZO8AbMBrAEEBAAtlrQBmAJkAgIA1sRw"
	.ascii	"AdAB8gEDAwAkiqwBcM4CAgLYAgIcMQCAARRABX8MQloCmAGrAgUFACSNtAHn"
	.ascii	"Ap4BAgIAFGeKAdUBhQICAgAgXXEBpwRpAgImSYKjArwCyAIDAwAUYYIBiAJV"
	.ascii	"CAgAK5i4AcIDjgEDAwAmZ4MBsgKqAgICAETB4QH3AX4CAgBPscoBrwGIAgIC"
	.ascii	"AGbU3wHHAo8BAgIA585GAewB2QECAgAQYX8BDnkJCQAMSGYB2gNZBAQAF3OY"
	.ascii	"AeoDFAMDACB/pAGMAiYEBABEepABtAKHAQICAOvnvwGOAj0SBTviuloC5AKZ"
	.ascii	"AgICAChphAHfA1wCAgA7m8EB+wOUAQMJlQIpVmgAvQKXAQQEAB6BogHrA6gB"
	.ascii	"AgIAMY+wAZUCxgEDAwDfzaIBuwKcAgICABdogAGJBE0DAwAzosgBjwPpAQMD"
	.ascii	"ADOftgGVAZwCAgIAMYiuAeICVQMDAMexdAG2AooBAgIA2dCuAZAClQICAgA+"
	.ascii	"n78B9AGEAgMDADKDoAHtAZMBAgIAMJazAQ8ANgkGCCAvArgBswEDAwBf3vIB"
	.ascii	"hgKQAQMDAEKivwGQA/EBAgIABjhbAdIDqwECAgA6oLwBlQPoAQ0CYxZvjwC/"
	.ascii	"AjUDAwDQrGgB6APFAQMDAE3K4wGfAfYBBAQAHnSVAfwDCgUFAAtIZAHZAYEC"
	.ascii	"AwMAFmiFAaUDuAICAgAgTmoBwgHXAQICADqQrwHkAbACAgIARK/HAdYDZAIC"
	.ascii	"ADmewQHqAiMEC4MBEVJzALYCXAcHAObCVQG5ApABAgIALl1EAeoCmwIFBQAV"
	.ascii	"W3wBpQIADwXlAhNMbgD9AagBAgIAJlZfAYgCjwICAgBBj60BAAAODIgCBBQd"
	.ascii	"APgBlgICAgAbb44BlAKIAgICU0SdvALkBGEGBgAKQ2MBmwRZAgIAB0lvAe4D"
	.ascii	"twEDBEQOZIwCvQG+AgICAESqywGkA4YCCwIMGk1jAuUBmgICAgCV6PYB0ANh"
	.ascii	"AgIALZi1AaoEZQQEABVGYwHSAaQCAwMAXdnnAYMEaQQEAFTX7wH9ATsDAwBQ"
	.ascii	"sc8BmQMAFxJXFWWEAGKPAQcGxAIuWmkC3wKSAgICACpfcwHuAakCAgIAPp/A"
	.ascii	"AdsDZQwCuAEPc48A+wGCAQICAFDH3gG4AsMCAgIATcrpAbUEXwICAAQ8WAHi"
	.ascii	"BNABCgTGARVTfACLAbsBAiBbNY2sAO0EugFTQRAIOVoA8gGDAQkCMCxhdQKu"
	.ascii	"AooBAgIALFFfAZkCnQIFAgUzk7AC9gNkAgIAW7vUAbQDygECAsgBEGiGALQC"
	.ascii	"MQICAM+sdwHyA5wBAgIAQpi1Ac8BhAEHCGMijKYApAReAgIACTBFAXnPAQIC"
	.ascii	"AERleAGUAQgFGRsEKD0AxwRyBAQACjtUAeIClAICAgAVPFIBoALKAQICAO7c"
	.ascii	"mwH1A6gCBQUAAwkXAdYD3AICAgAoTHQB6wNZAwMAFHebAewDnQECAgAfbowB"
	.ascii	"jQKdAgICAECEoQGcAn4FDmMhg6cA5gGHAQMDAC+RrwG0A7YCAgIAKkpoAeYD"
	.ascii	"TQICADCYwQH4AaMBAgIAE1JyAYcEVAICAAZdewHBAlMCAgDEqlsB7wGlAgIC"
	.ascii	"AEujwwGhA/sBBQUAHnmYAdEBwgICAgBDp8sB6gOhAQICADaPsAHoAcECBQUA"
	.ascii	"BiU+AecBxQECAgAhWGsBvQKZAgICACeIpAGaAXICDYkCNXSJAPwDWwICABJ5"
	.ascii	"mwGwA+4BBAQAHoqtAbICjQECAgBEkrgB7AM0AgIAQsLnAe0DtQECAgBm6PsB"
	.ascii	"oQLQAQICAMy8qQGwA/IBAwIJWdnyAqsCsAIEBAAghaYB3gO9AQoC0AIhia0A"
	.ascii	"wAPFAgICADNSZgG1AbwBAwMAWNfvAdYCqAECAgCuq3IBggG7AQUFAD602QHz"
	.ascii	"AfoBAwMAH1Z1AeUCoQECAgAtZ4UB6AKmAQICADxkegHzAaQBAgIAO6rMAZ4C"
	.ascii	"dAICANi4ewGTAYACBQUAG3GPAcYBqwEDAwCf+PwBlQHzAQMDAFDE4wGqAocB"
	.ascii	"AgIAMmxxAdUD8AEDAwAmja4BngGHAgMDABtujwHlAwUSBFEJUG8C9gOeAQMD"
	.ascii	"ABRXcwGBAagCAgIAEFFhAckCSQIDdcKeWQKlAhASBOACCDtaALkDtwECAgAX"
	.ascii	"eJUByQLZAQICBjY7OQLMApkBAgK6AVqJbgCAAYsBBQUAN6vGAeQCogICAgAw"
	.ascii	"or8BlwKbAQMCKleNjwKZAl8CAjeyiisCsAI/AgIA9/ShAbgDmgEDAgQFLkEA"
	.ascii	"zwM/BAQADE5sAbEBeRQPzwEsjqMCe7MBAwMAGnydAQFFBSkQDEdmALYEagIC"
	.ascii	"ADmTtAHdAecBAgIAb8/iAfQBSgMDAEnK5wG4AnsCAgD27pcBrwMxBAQAF2+S"
	.ascii	"AcMBogEDAwAph6IBnwHQAQYCvQENIjQCsgRlAwMAJIWjAaICUgICAPbpjQHN"
	.ascii	"BHICAgAtdJwBuAOnAgIC3wE/Y3sCgwRRAgIAC2KAAb0DogICAgA1VHUBhAI1"
	.ascii	"AwMARJirAbkD4gECAgxT0OsCjgJHBQTyAa6lWALCA9kCAiizAR09WACMAvAB"
	.ascii	"AwMAGktoAbsDvgIEBAARJUEB9AGqAQQEAB1ohQH5AUEDAwBHr8kBoQGEAgMC"
	.ascii	"kgFrwdoAqwK3AgMDABN1lAH7AaEBAgLhAT6bswJTswECAgAsWncBpgJ/AgIA"
	.ascii	"29KEAZ4EyQEGB70BJXGUAK0EcAMDABpOagGzArACAgIACV+BAdADrQECAskB"
	.ascii	"DG+MAPwC9QECBUIfY34CxQF2FgLBAS9ugQKvAoMBAwMA8e+PAdUDXwMDABh1"
	.ascii	"lQGYAkwDAwDuuFUB0wGPAQMDAD600QGYApYBAgIAPbviAagEKQMDAAxFaAGY"
	.ascii	"AbYCAwMAI4qsAfMBOQICAAo9UgGyA3YCAgB07vgBqgGhAgMDACePrAGbAaIC"
	.ascii	"AgIAGGeLAdoBsAEEBAAwnsABqgItAgIAp5+BAfkDYQUCBRR4kwB6qAICAgAU"
	.ascii	"RWYBvgOsAgICADdkggHNA1gCAgBe1/ABgAKlAQICABJQcQHiAZsBAgIATs7n"
	.ascii	"AfwDcAICiQFTmq4CrwNoAgIADleKAYcBewIH5AFAhZoCvAO2AgMDAAsfMQGo"
	.ascii	"A+4BAgIAM5e4AaUCoAEDAwDNlkABtQI7AgIA99iEAawDYgICAFfL1QGkA68C"
	.ascii	"CgZ8EjRRAqQD9AECAgA1osMBqQG8AQQEACicvQHQAqACAgInR5OxAJgC8AED"
	.ascii	"AwAQVXsBlASAAQICACBJWgHHAmICAgDStFQB7gH6AQICABFcegGNAXUFBQAJ"
	.ascii	"R2MBxQM7BQUAAR0uAbMD9AEKAp0CEF+AAukDBAICACyAogGrAbYCAwIPSqzH"
	.ascii	"AnykAgQC4wJzytsA+wFFDAKaAi+aqQKiBGoCCqwBDEJdArADYgICAGns/AGc"
	.ascii	"AbMCAgIASrfdAc0DxgICAgACHzYBuQKTAgICAAtdegGXA+4BAgIADld5AXq8"
	.ascii	"AgMDABdykwEDDYcqjwOcAQ4OANq0VgH/A8YBBQUAD2KCAYcEMwQdkAIWSl0A"
	.ascii	"0wLsAT8IXBkkMQDXA8YBCwn5ARZsiwLXA7kBAwMAV8HaAfUCsgEJCQDKnEIB"
	.ascii	"tALOAQsLAOHFcgHCBDcCAgBPmLcB8AJHQA2nAQ9LZQL5AZ0CAgIAZa/LAYME"
	.ascii	"cwUFAB5VcQH4Ac4CJQpcMnuZAM4EWgICADyRtAHWA8ABAwMAD2aLAfYCeQYG"
	.ascii	"ACtwgQEAuwFTKrYBAg0YAO0CQg4OAB9sigGLAd4BDAwAByg+AcEBywEDAwAv"
	.ascii	"QVcB5gPaAQkJACKStAGZAfYBOAjeASmIqACTA7gBBwcAH0hdAWLVAgkJAAUc"
	.ascii	"NAGbAecBAgIAXam+AdQERAICADmUsgHcApoBBAQA38JYAagCmQIDAwAziq4B"
	.ascii	"qwR6BgYAEjBIAbEC4gEGFwYaMT4CtQJxBgYA5sddAYUCvwECAgA1RDoBvQRS"
	.ascii	"AwMAJ42yAXjTAgYGABFEWQH3AaECAgIAXKbCAegC0wEGBgAUPVYBtAKVAQw/"
	.ascii	"mALSokYCjAQ+AgIAUbLQAdsCxwEEBADhvl0BqgLcAQYGACBLXgGZAsQCDwME"
	.ascii	"GWOBAP8C2wEXA7IBFztPAnaiAgICAFCluwGhAboCAwMAVtnqAZIB6wEDAwBB"
	.ascii	"kq4BlAN1CQkA2qpDAaYC9wECAgAxbYwBpQKtAgICAEuqygH+AZgCAgIAW6i+"
	.ascii	"AcwCzQELCwDhvF8BkQPOAQkJABdTcgGQAqEBAgIAppJtAdIB0gILCwAGKEAB"
	.ascii	"iQQMBAQAAxsuAYsC/AECEVQfYYEAGdoBGHnnAQMRHQDlAosBBQUA165XAcYD"
	.ascii	"+QEPBIwBGVl0AsEBtAIDAwBYx+gBlgOsAQICADwxHQG3At4BBAQAJWJ2AfYB"
	.ascii	"wwEEBAAcN0YBtAJNCAgA061aAaoByAIHBwA1iKkBxwOxAgUFABVBXgHjBGkC"
	.ascii	"AgAvepcB/gFvBQUAIYCZAY4BnAIFBQAfgasB/wGfAgICAEOcugHbAtkBAwMA"
	.ascii	"GjlJAYgEOQICAD6rzQFryAI6G8IBDj1YAr4D9wECAgA1qc4B+ALEAgUFADab"
	.ascii	"uQGGAsYBBQUAEEBZAc4DkQECLTImgqEAjAJhBQUAHoetAcwCXwQEAOzUdAHa"
	.ascii	"AbgCCQkAMZi3AZgCsQIMA1gOXnoAjgKlAUMDuAHEkT8AiQSfAQcHABtbdAGB"
	.ascii	"BCYCB8sCPqvNAOsCdAUFAN3BcAHNAyQlBd8CFGaHANgD2wEEBAAVc5IBzAQ+"
	.ascii	"AgIANYGhAUW8AhgYAAQYKgGkAo0CBQUACzFOAesCjAECBg46Z2cCmAKzAgIC"
	.ascii	"ADylyQG3AeIBBwcAIYGgAYkClgICAgAwgZwBjAL6AQMDAEvC3gHYBEwHBwAR"
	.ascii	"THAB+QGdAQICADOJrAGcAoYCAgIAQ5q1Ac0CfBAP4gLit08ClAGJAgMXiAIa"
	.ascii	"aIkC2gO7AgoKABM4UAHHA8cBAgyEAgpegQKbAboCAgyIAhVohgKxBK8BBAQA"
	.ascii	"PFxkAfcD+wFCCa4CAxwyAKcB4AECAgBMmq8BzwQsCQkADkhqAc0DcAQEAAYu"
	.ascii	"SgG+BFwEBAANR2gBuwRzBAQABBcvAbgCPwMDALuQUwHVAboBBQbpAS6bsAJ7"
	.ascii	"UQkt7AEDKUMA7QN8BAQABTlWAbcBkQIFBQAXaIoBzAOfAQICBgxGXwKEArUB"
	.ascii	"BAQA4L5zAdUC6gEGBgAOHi4BtgG4AgMDACR/ogGJAr0BAwMA0Ld0AYIEegIC"
	.ascii	"AEJ0hgGlA1ogAuYCF2+OAMEETwICACuDqAG1BLcBCASKAjdrgQCsBN8BNwZb"
	.ascii	"AhEhAJ0EeQcHAB5OZwHuAqMCBW6nASh4lALSA74BAgIAGnaWAdgEdUQOAAQJ"
	.ascii	"FAL0A9IBAjc9FEhjAswCAC4VBwIYKgKhA2wGBgDcr08BaIICDQ0ABCA1AdUB"
	.ascii	"ARJutQEEIjcCzgKTAgIDdSt3mgDPA5gBCwIKK2yFAnmdAgMDAB91lQGVBDsE"
	.ascii	"BAAtia0BlgKuAQICAOLBfgHTA9MBBAQAUNLuAd0BowIDAwApepoBogQPAgIA"
	.ascii	"GmGGAdUDxQECAgBEvNgBzAHJAQICACdieQFrmAICAgAoQFABgwJ6BAQALqPC"
	.ascii	"AbMEdQICADBUcgGGAq8CBQUACCE2AdcCmAICAgALQmgB5gF3BgYAByQ5AdMB"
	.ascii	"6AEFBQAcfJsB/wGHAQQEAD6jwgGFAi8CA5QBwrZ5AvwDOAI9eyGBogCZA8IC"
	.ascii	"BwcACzlWAacD1gEDAwALPVcByAPrAQcHACOKrQGwAY0CAgIAFmF/Ad4CnAIC"
	.ascii	"AgBEbHkB8gHlAQICADWcuAGeBKcBBgYAJlJjAc4CZgMDAMyvSgGmAhtfA+UC"
	.ascii	"BS1GAPwBuQEEBAA3gYkB0wOeAQICrQJLnrkA+QHNAQ4C9AEXZIEAsgKgAQUF"
	.ascii	"ALmKQgHGAbYBAgfFASyNtQCVApUCBAhHCC5CAJsEiAEGBgAHGzABuAPWARAK"
	.ascii	"vAIdfqEAR6EBBAgTGjE/AMoCrgECAgDdrVwB+gOjAQICAEKXtAGRAq8CAgIA"
	.ascii	"R6C9AZMCqQIEAlMqfaECABgEFwUFIDAAkgKyAgIe5AIcZYQAvwR5AgIAKz5Z"
	.ascii	"AdsC1AIIFwUtlLcA8gHOAQQEABNyiwHhAw0FBQAHS2kB5ALLAQICALuQVQHT"
	.ascii	"ApYC"
	.ascii	"AgIANIWlAecEbwQEAAg+WQGfBDsCAmNkudIAwAJEBgYA4LRWAagDYgICAEWs"
	.ascii	"wgHUA5wBAgIAGGN6AZgEEQMDABBUdQHJAqcCBAQAFWyIAeYCXQQEALyuiQHl"
	.ascii	"AfkBAgIATaXBAdwDhQEODgAEM1IBngLAAgMDACmOqQHtAdQBAwMAZNzxAa4B"
	.ascii	"1QECAgAYPksBvwNWAwMAHX2lAbMDtAECAkhc0OMAswKZAgUC4gKY9P0AwgJ1"
	.ascii	"AgIA7tyiAYwEvAEEBABQ1vEB7AOQAQIOZCJmggLAA6oBAgIAGW+HAbwDlQED"
	.ascii	"AwAaW3kBT4wBDQ0AAxUnAZoDnAIICAAJGSoBhAKmAgICAEJ9mgHLA9QBAgIA"
	.ascii	"KJS1AYUCnwICAgAylLEBqwInAwMAO4+pAfoBqAIGBgApgKEBzAORAQICACZL"
	.ascii	"WgE7QAIhFAs8VAD0A78BAwMAQ8flAYcC/wEDAwAsl7kBiwQzAgIAL5GsAYQE"
	.ascii	"KQoCUAhObgDMA9kBAgIAWNXxAYgD7wECAgBNv9sB7gHHAQgDBTCLpgKKBCAF"
	.ascii	"BQAMUXMB2AH5AQQEAB57nAGUBC0EBAAIP1wBugPOAQICACqHqAGvAi8DBpwC"
	.ascii	"5cWNAswD2AEEDYUCD2mKAKsBJgkJABZcegGqBKwBBAQAMlZkAeEBkAEpAjEe"
	.ascii	"YX4C4gKXAQII1wF3cE8CJ2oEHS8FK0EA3AJaAgIArppTAfwBsgECAgDDw4kB"
	.ascii	"7AGbAgQEACaOtAHyAdICCwsAAh00AcMDbgISmwIPWHsAyQNeBAQAFXSRAaIC"
	.ascii	"pQICAgAsm7gB7QRrAwMAFmaJAaAEGQMDAA43WQGjBLQBBAQARUEzAaYDnAID"
	.ascii	"AhY5TmIC0gHVARQJhAIfgaIAqwGmAgICACSAmQHzAdgBAwMAHHCPAZkD5QEC"
	.ascii	"A+8BOp26AvkD2gEEBAA3q9YBjQH0AQMDACVfdAHsA8YBAwMAXeX5AbcB2QEC"
	.ascii	"ArgCd77VAIoCNAMDANO4ZgGLAioCAgCQoZYBvgHBAQICAEnG7AG8A6YBAgIA"
	.ascii	"IICYAYAEyAIDAwAbNEABuwHOAQICAAYhKgHLAtYCAgIATsruAeoB5gEEBAAX"
	.ascii	"gqAB9AGDAgcI5AIkfZ8A3gJQBAQA0q5gAdcCjwEEAvcBvKFMAq4CQwMDALiU"
	.ascii	"SwGNATYfBOoBC0djAMQCEwcHAAMkOwG/AaMCAgIAgM/hAZ0BB10LXgMsRAKJ"
	.ascii	"AfABAgIAMUJQAfUDsQEJAs8BDmSEAKsBsAIGBgAniq4BvgLYAhgaByF5nACh"
	.ascii	"A9kBAgIACDdNAdoDpAICAgAnPU8B0QOeAQICACZgeQG0Ai0CAgBXgnsBhAP2"
	.ascii	"AQICAHLU6QHRAkoCAgC5nVYB3gGoAgoCUySSsgCuAYcCAgIAVsXUAeICfQIC"
	.ascii	"APDNfQG+Ak0CAgDy2o0BwgOYAQMDAA8qPwGcBD0CAgAVYHwBrAKYAQICABs5"
	.ascii	"RwGXBF4DAwAQYIQBvwHQAQICAE+RogGVApMBAgIAP7HNAbAD0AEKAsMBBE9k"
	.ascii	"AtkCgQIMDAADDyMBuwKMAQMDANvPhAG9AewBFAhAJIOlAoIE3QEFBQAdeKAB"
	.ascii	"hQJsAgIATcTiAa4B2wEEBAAweJQB/AL0AQIC5gJRocICwAOmAQICAGe90QHR"
	.ascii	"BGgJBAQIPlIAkAGoAgICjQFGi6oA9wHdAQICAF/N3wEnkAEMDAACDxoBtgKW"
	.ascii	"AgICAEC60gHAA5IBAgIAQnOEAYMCWAQEACuoxgGPArICAgIANIyrAf8BqgEC"
	.ascii	"AgCvmV4BnAS6ARcCAxlGWwDwApsCAgIAMHuYAeYB7gEFBQAbhKYB/wLmAQIC"
	.ascii	"GF2LnAL2A2UCAgBpzOQBsgHVARICzQEqgZ0C8QGBAgICAKHj7wGRAZACAgIA"
	.ascii	"bMjdAYcCoQECB+cBrIhLAI0D6wEDAhNKztgCyQKWAgQEAA1ScQHYAlwCAgCy"
	.ascii	"lVUBgwNzAgKmAayuggLCArgCAgIAMYmwAeECmAICAgA5YHEB1QGqAgICAFie"
	.ascii	"tQGQBD0CAgAvlrwBwgRsBAQAJHGSAZYCWgMDAL+zYAG3A60BBgYAIo6sAbEC"
	.ascii	"lAICAgA8pcABggIsAgIAQlhPAZ4CmQECAsoBIGN3As0BgQICAgBp2OYBzgO7"
	.ascii	"AQIC+v8DEnOZAu4EtQEHJ2QIOloAxgONAQICACZddQGEBNMBAgIAVtD3AY8C"
	.ascii	"JQMDAEOJoQGJAowCAgL+AUyYugC0Al0DAwDv02EBlgGnAgoJjAImlLsA8QHt"
	.ascii	"AQICABlsiwHxAacCAgIALYeoAZgDgQICB50CGl53ArYChwECAgD6+9kB6ARh"
	.ascii	"AwMAFE9zAZcCNAQEANWiSQGiA/4BAghNOp69AJQEzAEDAwAqkbYB9QHeAQ0C"
	.ascii	"ggIddZYAywG/AQMDAHPu9wGJA+YBAgIAI2p7AQcMXwLPAgovQwAsUAgIABxT"
	.ascii	"bAG9AjcDAwDQokgBrgTCAQQEABtlgQHzAYIBAgIADitDAeoClgECAgAtXFkB"
	.ascii	"0gKQAgMDAA44UgH4AesBAwMAEHaXAYUElAEEBAADEycBgAPxAQID5gJBqMcC"
	.ascii	"kAKQAQICADaw1gG5A6YCAgIACyEyAfQBDRIZ+f8DAyE2AL4DqAICAgAIIDMB"
	.ascii	"kwSLAQICABVDXQGtA2wCAgAfV1sBmQG6AgICjQJf4fYAswRYAgIAOpW8AagB"
	.ascii	"2wECAgA6dpABoQKqAgICABVcgwGrBGACAh1MjqwAmAHxAQICADyZvAGrA3EC"
	.ascii	"AgApa3oBjgKUAQICXBR+qQDRA7ICAgIAChknAeACnAIGAmgthaUCoAI/BAQA"
	.ascii	"y5pMAUJzCQkAChAXAf8BMAICAChYbgGeA9wBAgXGASNqhgLMAdEBAwMAIH6d"
	.ascii	"AfkBAjAHPgQpQQDSAd0BBAQAE3KQAYsCtgICAgA+mrUB7gObAQIE1QIPVnYC"
	.ascii	"LGMLBIIBDj1VAKcDiQECAgBag3cBygREAgKTATN7nQCcAqMCAgIAVcXiAcQC"
	.ascii	"sAIFBQAYcpEBjwGFAgMDAB9xigHgA2sEBAAjiaMB3gGmAgIE8wE1pMICuALV"
	.ascii	"AgICADWiwQGGBE4CAlxHt9kAnwOvAgICAAgjPAGPAlkDAwA1k7YBxAHTAQQC"
	.ascii	"4AIRXnwAvQODAgMDAB1IYQG+AlECAgD36KgB0gHwAQIDrwEcdpUAnAP9AQIC"
	.ascii	"ADSQrQHAAsYCAgIAGk5tAYMD6wECAjlUtNYCowKFAgICzgFupMICtwIyAgIA"
	.ascii	"v6+CAckCoQICAgAulb0BiAJjAgb+AUjI2wLpAdgBAgIAD2iJAdgCUQICAO7V"
	.ascii	"oQGTAv4BAwMAH5G3AawEwwEYAsoCETdNAsIEdAMDAAQiNgGxAo0CBAQABTFM"
	.ascii	"AbcCqgICB4kCDF6AAO4DhAEHCzsGNFIAxAKPAgQEAA1FXQHOAdcBAgIAF26R"
	.ascii	"AYcErgECAgAnf50BwAK8AgICAAdafgH+A6IBAgIAD3qRAbgCkAECAgAfV0wB"
	.ascii	"6wMMBAQAB05uAb4DxwICAgAJHTYBvgGyAQQEADuvzAGFArkCBQKRAi5QbgKd"
	.ascii	"Ap8CAgIAMZ26AZwB8gECAp4BFGeIAKYCgwECAgBUjIcBygJAAgOQAffanwK/"
	.ascii	"ArwCAgroASN1lgKbA2YEAtYCvLBvArUDpgICAgAlNkIBjAGNAgICABFbeQGI"
	.ascii	"AuwBAwMAFGKKAeICqgECAgAqPU8ByQKZAQIFngIxmLsAwAOcAh4ErwEPKT0C"
	.ascii	"rgKzAgMDACePsAGiAs4BAgIA5M+bAYsEyAEGAgwihawA2gGKAQQEAB+CnAGK"
	.ascii	"AcgBBAQALZS0AZ4EZQQEABRafAHOAaUCAwMAVNDhAY4D8QECAgAKOV0BJCYI"
	.ascii	"CAAMRmMBnAQdAg62AQQ9YQCqAjECAgDWo1EB4gIAAyxcAyM5AKsCiQECAgAm"
	.ascii	"T1oB/wNrAgIAUNPnAa8DCwQEABhtjwGXAowBBQUAF3yeAd8DXwICAC+ZvgHY"
	.ascii	"AaICAgIAXNHgAZUEtAEDAwAQVnIBrQJYBQUA6claAYICXwMDAC6z0QF4sAEE"
	.ascii	"BAAZcpIB5wRnAwMACkRhAaYEYAICAAgtSAGlBGICAmotWnkAzwNcBAIPE2+L"
	.ascii	"AMQDVgICACV9oAHWAX0QAhcud5AAmgQ5AgJ9fcfaAuQDuAEOArIBDmOMAIIC"
	.ascii	"jAECAgBEpcQB7ANVAgIAOKbIAZYCjAICAgAcbYgB7gHEAQICABY4QwH0AeAB"
	.ascii	"BgdIFXKVAqoCjgEKAo0CIHCRANYDVQ4C1wEaeZ8AvgPrAQICABBwmAGZAwAC"
	.ascii	"Cg0RVG4CeM0BDgIJSnmNAL8DrwICAgATPlwBSggJEQcMO1EAqwOjAgQEAAYS"
	.ascii	"IQH1AYECAgIAKH6PAbUCqQIDAwBNzewBuAKCAQMDAPfpbwHyAZMCAgIAc9zt"
	.ascii	"Ad0BqwEDAwA9iqcBnAKpAgICAEK02AGbAmUDAwDnwlQBYZYBAgIAK1poAfYB"
	.ascii	"mAICAowCJYqtANAEcgICADaBqwHUAkwCAgDWs3sBwwIGBQUABS1GAcMCmQED"
	.ascii	"AwArj6QBmgKTAgICACM/YQHqBOUBBgYABThbAdIENwICACdmhQG4A6ICAgIA"
	.ascii	"DyQ2Ab4DuwIDAgkfOE4CtwO0AgMDAAofNQHpApsBAgIAHGZ5AQMOpCSVA5MB"
	.ascii	"CQkA7MZZAfICXQYGABc/UwGGA6sBCgoA1rJYAbsC1QEFBQDXxYYBtANNCAgA"
	.ascii	"CC1DAa4CxQEKCgDpzGcBqgKgAgYGABhpiAGgBDMcJ+YBGmOFANUDuwECAgBq"
	.ascii	"zeUB+wKQAg0NAAckPAGNAsMCAwMAQZq8Ac8DygEsArEBE2mKAIACzwITFls1"
	.ascii	"dJEA0gH1AQkuQTCRsAD5A8QBEATeAgpYeAD2Aj4RGJ8BCjRKAtUCtwEKCgDT"
	.ascii	"mjoBpAHzAQICAGe1yQFZywEICAAGGC4BiAOyATwCrAIpa34ArgSNAQ4OAAUK"
	.ascii	"FAGZA9kBBQUAEUFaAe4CgQIEBAA5KCcBrQLjATwCADQnIwK6AcQCDiSSAgMl"
	.ascii	"PQCgA6QBBQUAITRAAfYC/AEFBQAWGCIB9ALxAQICADhMWAHQBE4CAgAqi7IB"
	.ascii	"pQLcAQYGABJAWgHAA6cBCCdBKZOzAKgC0wILCwAkgqMB6gLvAQUFACkeGwHx"
	.ascii	"As4BBgoSLyssAIoDvQEFBQAfQ1QB6wJECQkAHnOVAfcCLAsg2gIYVXIChQRB"
	.ascii	"BAQAED9SAY4EEwYGAAg+WwGgA30HBwDiul4B+gLMARIJZRU9WADAAaQCHQ/g"
	.ascii	"ATGWtQL2ArcBBgYAzJc3AQ2QAg0NAAQJDgG9A7YBAgIAWajFAY0DtgECAgA3"
	.ascii	"QDgBlwHjAQICADhWawH/AZMCBQUAK32bAaoClwICAgBIlL0BjgOyAQYCowIt"
	.ascii	"PD0AuAQhPAIzDjlUAqACgQIFBQAiZoUBjgHsAQICADp9kgH8AncCBg2GknEC"
	.ascii	"wwHpAQIklAIrkbACxgHKAQMDACladgGCAoACAgShAR9khQDOBFEMBWsGNlcC"
	.ascii	"wgGGAgkJACF+oQHFA6oBAgJagN3yAMsE6AECE6wBAyZAALAC7QEKEL4BDTJI"
	.ascii	"AMUEKwICAC1mggFB3QI4GmAEGjEAwANfBAQABkRfAdUClgEFBQDlx2ABjwPZ"
	.ascii	"AQMDAC1lfwHAA7ABAgIAW8XcAd4CxgEEAqwB7dhmAIcD3AECAgAxX3oBgwQr"
	.ascii	"AgIAVs/tAZwDRgIYXhFdfQDoAWYCAgAuVWMBjQTnAQcHAAQdNAGMAoMCAgIA"
	.ascii	"Oo+1AagDbQICANvFjQH0AyELCwAPWXkBhAQOAwMAAyQ3AfwDRQQEABpmgAHO"
	.ascii	"BFECAgBBrMgBXrkCAwMAECg+AaQC8QEGBgARQV4B2wLOAQUFAMinVQHJA50B"
	.ascii	"AgIARIarAegD6AEHBwAlhKkB+wIBLQ+sAgczRwKeAe0BBQUAIXiXAcMEhQIK"
	.ascii	"CgACChoB2wRSAgIAH2qIAYAEcQICQFWIoQK7AecBAgIAPKS/AZMEZAICAC+r"
	.ascii	"wwGeAbgCAwMAUdfqAcIBCDsVVwIdMgCjAd4BAwMAO26AAcgD9gEFCdYCJXOT"
	.ascii	"AMYEVAYGABBSdAFgyQIEBAAdUXEBnAHnAQICAGizywHQBFUDAwAQVXsBjAHV"
	.ascii	"AQQEAAwsRAGbAroCAwMAHFp9AYgEcQUFAB1ifgGPA94BAgIADCozAawEfQIC"
	.ascii	"AC9HYQG7At0BAwMAL2qAAbMBowICHrgBMIytArEB5wECAqABUrHLAJgCsAIC"
	.ascii	"AgBCttwB+gFmBwcAKZawAeEC2gEGBgAMNFQB4gPYAQMDACirxwEHsgITLQEB"
	.ascii	"EyEAvwG1AgMDAF/S8gHMAycDAwAmiq8BwwOtAgICADFZbwHIAtIBBQUA7MVo"
	.ascii	"AYkCrAIFBQAHIjUBpQHsAQICAEqiuwGfAcoCBQUAQ5GwAYwCuQEDAwDx4pgB"
	.ascii	"hgNUBQr4ARNiegCbAdgBBgYABCI3AesCrwICAgA2n8EBkwFGBx0BBCpFAP4D"
	.ascii	"9wEKCgACFScB+QLvAQMDACFZcAGiAqUBIAa1AcGLOQCPBIICCgoAAh40AXYJ"
	.ascii	"Dlu8AQMYKQLbApsCAgIAIDZHAXR8BwcABCtDAeMDQwMDAAQ+UAHcA7ECAgRf"
	.ascii	"LElXAo8BuQICKo4CPnyTAs8CTAITtgHPpEUC7AJ5AgIA9N9+AaABvwIDArgB"
	.ascii	"C2J/AswEsQEFKgcCDhwA5QKlAhUDswEhbIwAgQRbAgIAOZvBAawDVgIFqwIX"
	.ascii	"WHMAkAQ1BQUAHnWXAeoCtwIDAwAZdJABpwKPAgYGAAgwTAHxA9UBBQUAIoqu"
	.ascii	"AaMEfgMDAB1DVwHdAb4BAgIAJJizAfYBoAICAqgBidXtAPgCeQMDACaBlwHw"
	.ascii	"AcIBEgIABTBBAAEVBgYABBgkAdICgAEDAwDQokEBuQLpAQMDAFxLPwGQAZQC"
	.ascii	"AgIAFFh0AegChwEEBADduGABiwK+AQICwAHo0JwAsQLeAQMDABplgAGsAaMC"
	.ascii	"BAKiAl7D2gC5AcIBBAQANbPSAbsB0QECAgA9c4oBiQRiBAQAIHqfAYMBlgIo"
	.ascii	"ArwBHHSWArwEVgICADuWvgHdAfgBAgIANJvAAcQCdQMRhwHjymYAgQR5AgIN"
	.ascii	"YJChAssEQB8CBAtFZwKuAnEDAwDsz1cBngKOAgICACpbbwH+AZIBBAQAFzNL"
	.ascii	"Ad4CnAECAgDv01sBTqEBAgIAHz9TAb4D4AECAgANYoQBugReAwMACkZhAZEB"
	.ascii	"6gECAgBEiqcB2QQxAwMAFFV0AZAEIAICACttkAG6AZoCBQUAKo+1AbICmQIC"
	.ascii	"AgBq0ukBiQSiATUCzgEYM0ICpgLEAgMDABBiggGvBBQCNVgQSGYC9gGeAgIC"
	.ascii	"AB92lwHtAosBAgIARGhlAcEBzAECAgAkKD0B0QRIAgIABUNfARWTAkIQywIC"
	.ascii	"EiAAkAK7AgQEABVeeAHXA8YBAgIAQ7LQAdYDxAICAgAoSWYBmwR2AgJvPWuH"
	.ascii	"AM8DmwECAgBFjp0B9QG/AQICAEtzhgG3ARoDPysIPFgA8wKAAQMDAB5neQEg"
	.ascii	"wQEyE10DCxQA6gGXAgICACqKowGNAs0CAwMAMoytAd8BzQEHBwAohqUB0gOZ"
	.ascii	"AQICADyFmQHXAycFBQASYH8B1gHzAQICYnXR7AK6A78BAi/zAR57mwLsAlIF"
	.ascii	"BQAkX4EBiwLIAQMDABAzQwH3AawCBgYAKoCgAYQEVQIE1AIog6oAdtMCAgIA"
	.ascii	"G2N3AeMDxQIHBwAQNE8Bd6ACAgM5XMfbAtkD0AECBwQXZIsAhgHQAhYIwwEL"
	.ascii	"QWECmgKFAgICWGG82QDUAcEBAwMAIIakAeICmgECAgC2gDQBoQNcBQfeAhV4"
	.ascii	"mAKsAYwCAwMAH2+UAYUCxgIPBwskcpECjAIrAgIAwrSPAeIB3gECAgA2lLIB"
	.ascii	"wQOpAQICACR3jAG5Ac4BAgIACiEsAYYEugECCo4CV+L7AIwE3AEDApIBG1Jw"
	.ascii	"AFADBUkVByU1AuUCkQEEBADQplUB0ANJNQIDGW+QArQB2wEVBFQggaEArgEA"
	.ascii	"HgguCkZiAKEDZQICbs/EfACzAewBBwjJAR19nALBAe8BAwMAG3CTAckDngEC"
	.ascii	"BGQSU3sCiwKpAQYGAMeZSgHJAmIFBecBzKtBAoEE0QIHBwAPLEIB6QHpAQIC"
	.ascii	"pwJErckA3QJBBQUAIWiAAdAEIwICACZUbwGXA+gBAgIAVcbgAf4DdQMDACNX"
	.ascii	"dAGcAqEBBAQAt5BXAYkC+AERArQBTcPfAs8B+gEDAwBBt9EBhQQiAgIAJ3yf"
	.ascii	"AZwEgQECAgAuUWEB4QJLAgIAKV1iAYICcQMDABZ7lQFulgIDAwAnVmsB0QO9"
	.ascii	"AgYGABA8VwGpAb8CBAQAJoitAZcCsQECAgDCmksB4QKWAgICuAJZjKAAjAKQ"
	.ascii	"AgMDAB9zkgHVA/YBBwLKASJlggC+BLgBAwMAUVddAZkDpAECAgC/pnAB1wRt"
	.ascii	"CQO/ARJWdwCfA80CBwcACjZVAfcB0gEFBQAYco0BgQSzAQUFABFhggGHAmwC"
	.ascii	"AgCC7/wBuQOoAQICADOfuwGxAYgCAwMAad/oAeIB5AEEBAAce5wB1AOPAQgI"
	.ascii	"AAYtSgG3AokBAgLoAcOXaQK6AsUBAgIA16paAcQBuQELAgorlrsC8gLRAgIY"
	.ascii	"GyNkfgKRAqEBAgIAuZ92AbQCQwMDALKPRgHHA5cBAwMACSQ+AZ8CxwIDAwAY"
	.ascii	"W3kBqgHbAQIC4wFEmLYC4wOTAQMDAAQ1UQGdApsCAgIABC5IAZECiAIDAwAg"
	.ascii	"cJIBtAKdAQUDvgHEm2EAnwGVAgICABVliAGrBMIBAjRaAxswAK8CAgJBmQId"
	.ascii	"UmoCzQRYAgL8AUmcwAL7AXYEBAAliKIBUr4BBAQABRUnAYcB7wECAsQCUGFt"
	.ascii	"AosEiQEGAhMGO1cAxAORAQMDAC5LZAH7AcsBAwMAGGeIAagDigECAgAtanYB"
	.ascii	"ogQRAgIAJ3+qAdkEYAIngwILJz4CxAI6BgYA0qtaAbwBxwEDAgc/cooA+AEv"
	.ascii	"AgorHVRrAq4CQQICvgGhfkQA/gEUDg4AAh40AdQERQICAD2atQHwAusBBQPe"
	.ascii	"AgcVIgCtAk4CAgDDnEkB/QG3AQICAEV0bAGHApgCAgIAFWaEAcoBXhISAAIg"
	.ascii	"NAHPAb8BAgIAeOXyAZkCtgICAgA8lbUB/wGnAgICAC6UtwHOApkCAwMAC0to"
	.ascii	"AZABjgICAgBPq8YB2wGpAgMDACKAngHnAl8CAgDQwJcB1QKaAgMDAAo5VgG7"
	.ascii	"AlcFBQDbtmAB4QLQAQIDzQEuRDkA8ANQAwMAIpKyAawEZAICAAM4VQHHA3QE"
	.ascii	"BAALT3EByQLTAgMDAFrU9wGsA14CAgAjiqwB0wJIAgIAv5tQAeICnQICAgAN"
	.ascii	"V3wBzAH2AQICABB3lwGkAboCAgIAY+H2AegDdwcCwQEEN08C1wJZAgIA9uGK"
	.ascii	"AYkB7AECAtwCM0BXAoIE4wEDAwAud54BrAGqAgYCUiZzkwCMApEBAwMALqvN"
	.ascii	"AegCwgIICAAmjKoBhwGEAhECBBVohgKyAdkBAgIAOYilAakC2wIsApMCJGWC"
	.ascii	"AOECTwICAMCtdAEfAQMx9QEJNk0A4QMABAi6AQdKagCSArUBDAIJ2LpvALQC"
	.ascii	"TgUFANayYgG2AZICAgIAJXqcAf4BhwIFBQAuhKgB/gGeAgIC2wFxwN4CsgGA"
	.ascii	"AgICAFW+4gHRA/wBBAIkBClCAJkEDRECCg5AXwLsAm8DAwDdxXIByQKsAgIC"
	.ascii	"ACF6mgFKqwECAgAcLjwB+QGvAQICDcu7ZwDRA80BAgIKQbTNANgC7QEFBQAH"
	.ascii	"IDQBggK0AQQEAOHEdwGAAroCBwcACBwzAdYB2QECAgARaoMBiAHyAQUCaDRq"
	.ascii	"fgL6AZ0CAgIAbrXSAb4D5gECAgBIxN8BggKgAgICABx3kQHLAsABAgIAs4s1"
	.ascii	"AfoBtQECAgA1f5oBqgPWAQICAAk4TwH6A5kBDgK0AStleQCpAoIBAgIA2tWK"
	.ascii	"AYcE2wECBTorfaEC6APGAQICAF7d9AHUA3YGBgAIN1MBnAIxBgYA1qZPAcsD"
	.ascii	"rwIFArQBBRkrAOUCTwICAClfcAGTA8YBAwIOBDZTAOsCkwECAgA6YFgBtQHb"
	.ascii	"AQICABhqhAHiA2ACAgBFyd8B7QRuAwIcImGFAMgD1wECAtgBQ7PVANsBowIC"
	.ascii	"AgArf5oBigInAgIANG+SAYcD7gECAgBBtNMB0APAAQICADWdwgHvAYMBBAQA"
	.ascii	"Cyg+AasCLgICAM+xfQHpAVsCAgA9bX4BywOyAgIC0AIzVW4C1wKVAgICADOF"
	.ascii	"pgGKA+UBAgLhAXyyzQLBBDYCAjpzvtwCpwHfAQICwAKE1eoC7gHiAQQEABZ+"
	.ascii	"ngHaAlUDAwDmzGUB+QNSAgIAFXaZAbIB7wECAgBjudEBxwKHAgUFAAQgOAGu"
	.ascii	"AjECAgDux5oB8QHZAQICAA5cfAGUArICAgIAGmyUAUN3AzKxAQUTIgLDAnMD"
	.ascii	"BD347rcCtQSyAQQEAD9eaQGcA94BAgJBXaa7AKsBzgICAgBCeJIB9APDAQMD"
	.ascii	"AFjf9wHRA9cBAwMAWN33AaEEaQICABdegAGuA3ACAgAFZYsBzQHoAQICABRm"
	.ascii	"gwGpAdQCBQUACThTAfEDfQMDAAcyUQHFAkgDAwDrvF8BsQOrAgUFAAkZKQHv"
	.ascii	"Ap4CAgIADV6CAYcCoQICAgApfqEBngOiAgICwQIxPlMA2gHjAQICuAFFsccA"
	.ascii	"gwLRAQICAAxXdgGcBK8BAwMANlVfAeMCYQICAMSoYAHIAewBAwMAJ4uyAYgC"
	.ascii	"wwECAgAYNkcBnQSmAQQEAChbawHEA3wEBAATZIQBmQHAAgICABNxjQH3Ad4B"
	.ascii	"AgIAbt3vAaYBqQIGAiUxhqgAiQPjAQICjQE/go8ChgK5AQICANS3bQHPApQC"
	.ascii	"AgK/ATyNrQDhBEwDAwAHNlcBpQNYBAQAG3+nAYsEmAIEBAAGIDsBnQKSAgIC"
	.ascii	"AAcnQgEDD9Ac+gKAAQwaf9GnTACYBFAGBgAUWHkB8AJjBAQAJUlYAaIERAYG"
	.ascii	"AB11mQGcA+4BCT1aBxkuAu0CmAEYGZkCy6JMAo0DogEDAwDs13MBkwK7ARgF"
	.ascii	"tQHv0GkApAPMAQcHABlxjwGsA5gBCAgAG1VrAZsDqgEEBAAYLkMB5wGEAgIC"
	.ascii	"AGSu0AHrAuIBBwcABytHAYQDnwIKCgAEHzYB0ALeAQYGAD43NQGgAtkBBwcA"
	.ascii	"HEVdAcYBkQICAgBXtdMB8QLKAQQEAFY/NgG3BDoCAmlNlLACiANDBwcABCU4"
	.ascii	"AbsEcwNMjAIECRUAwwO7AQcHAC6cuwGpA7UBAgIAPZSuAcIBqgIGBgAqjq4B"
	.ascii	"sgKhAgUFAB59mQHTA7gBAgIADXGQAYQDuAECDZYCEzhNANABugICAgBGtM8B"
	.ascii	"/gPNAQQEACOMsAHgA8YBAwyIAgtceQD1AjETBUwKP1oAsgLOAQYGAPDVdgGX"
	.ascii	"A9oBCAIFEyk/AKUB8AECAgAccIMBpALlAQQEAAsvRwHnAYgCAgIAIniKAcoB"
	.ascii	"hAICAgAYYowB+ALDAQIotQEPJz4AxAQ+BgYAEFp6AdMEywEGI8kBCjhUAIEC"
	.ascii	"kAIDAsEBUKO8AOkCggICDA5TODEAA9wCoAECaQcfNAD+AncCAgA6e3kB0wGL"
	.ascii	"AgICAE+tywGmA6oBAgJ9aKm/AsMESQICACZ3mQHXA7sBAgIAgOb4AaIB2wEC"
	.ascii	"BrABRHyNAK8C5gEDAwAVKC4BmgOEAQUFAO/CWgHIAfoBBAQAIH+fAaUEMwMT"
	.ascii	"fiNxkgCXBOoBBAQACSxIAboB/gEDAwAcdZgB2wLPAQICAN2/fAGVBEMEBAAP"
	.ascii	"Q1cBkgO6AQYGABRFYQH7AlcGBgASOUsB0AHKAhUOYgMiOgCYA80BBQUAF2F9"
	.ascii	"AcAC1wECC4YCLWSBALgB5gEDBjVHtsoCxAObAQMCDSp7nACSAvYBJAK4AhpS"
	.ascii	"cgLcAuQBAwMASTMoAa8BuAITA7ABKIurAsMDrwECAgAbe5MBtgGzAgICACF7"
	.ascii	"pAGBApcCAgIARJezAaMDfgICAMqgRgH8AroBAwMA3atCAZ4DdwICAOfOdgEA"
	.ascii	"4QEZMecCBAkNAI4CpQIFBQADJDoBigLNAkRDoQIoeZkCiQHdAQsLAAQkOQHM"
	.ascii	"BBUCAgAqXncBzAP0AQcFuAIba4sAwwQMBAQAFDdWAZEDrgECAgDXunoB1gOw"
	.ascii	"AQIGaRl5mwBiyAECAgAmR2cB0wGqAgQE6AEoh6ACxwGeAgUFACWWtQHkAf0B"
	.ascii	"AwMAJH2iAYcEygEEBAARZogBuwGzAgMDAFfP7gF+ewUFAAg5VAGhAp8CCAcv"
	.ascii	"FmiJAp4B6QECAgAxh6UB2AJ1CgoA68NYAbkC4wEDAwA8LiUBxQMiBgYAFGqG"
	.ascii	"AeECzgECAgDSq14BgALBAQUFAA9AVgG6AqQBAgIA0p9WAc0CYQMDAO7edQHx"
	.ascii	"AygGBgASX38BmwOhAQICAK2QTgHNApMBBQUA6N5tAewCXQICAClARgG4AaQC"
	.ascii	"BAQAJIimAdMDyAIEBAALJTwBggGTAgUFABplhgH7AqkCAwMAOmyDAaoERwIC"
	.ascii	"T0KNrgDDA6kCGQIAHD5QAKUDZQIUB9G0aQDwAv0BAwMAPSUfAdAEUAICAD6p"
	.ascii	"yQHbAbgCBgYANJ+/Ac8BqgICAgAeao4BkgSgAQYGACRRYAHmAWMJApgCVJqu"
	.ascii	"AJAB7AECAgBHnrgBT6QBAgIALmmIAYEEwgEWA7wBClZ2AqgD3wECAgAlnMAB"
	.ascii	"mgG2AgIhhwIyja4A1wPKAQICAApgggG6A8ABAgLpAUOszQAAjQE3P5cCAw8b"
	.ascii	"AvcC/QEHAxgHEhoCsAR6BAQAEytDAccBHgUXygEDMUoAiwK0AQMDAOXNngH9"
	.ascii	"AlgXApMBFGN7AmvPAgcGvgEFHjYAmQR5AgIAFDlRAesBiAICAgBxydkBmAHm"
	.ascii	"AQICADx5jQGLAi4CAgDIhC8BclcRHSkCHTICX8YBAgIAKENdAfkCSwMDACNQ"
	.ascii	"YwHSAZgCAwMAGn6fAf8BjwICAgAufJ0B7wPrAQQEACx8mAHIAwReAlIOVXQC"
	.ascii	"wgOoAQICACV4jgH4A8gBAgIABlx9AbgB2gECBfQBFGaGAu8EJQkmOws6VwDz"
	.ascii	"AvcBAgIAMzM9AeYD8QEDAwAuco8BrQLYAQME4QIkVWUAvgGQAgICABNXhgHJ"
	.ascii	"AmsFBQDnw1gByAGTAgICPVuoyAC2Ae4BBgIWHWaBArYDzQEFISsffp8C4gKX"
	.ascii	"AQMDAL6NPgHkAooBAgK4AbmQOALUBDIDAwAJOl4B2AS6AQgIAAIPHQH+A0QC"
	.ascii	"AgAwe5QBtwHTAgYGAAgrQQGaAvcBAgIAF2mLAf4CPywHlQEFM0sC/ALwAQQE"
	.ascii	"ABphfwGDAqwBBAQAzZlBAb8BlQIDAwAnmrgB5ALEAQMDAM6eOAGrAd8BCQim"
	.ascii	"AiB/ngKFA80BBw2yARNFYwLfAfIBBgYAIImqAYsChgICAgAUW3gBgQR+AwMA"
	.ascii	"CC1DAdQClgECAgDbtkYBLt8BQgdfAREhAqEEhgEFBQAKEyUB9gHXAQICADCI"
	.ascii	"pgHaApgCAgIAIlx1AeABxQECEWQija4AigKMAgILURxtjgLCBFkFBQAPS20B"
	.ascii	"owKBAgICADZ5mQGYBHsCAg1SeIwAiQO3AQIDSzk+OAD4ArIBAgKtAbiBFgDM"
	.ascii	"A50BAgIAaKC7AcIByQECAgA7aIEB2wQ5BA8CDUdoAKYCiwEDQZkCyZdEAMsC"
	.ascii	"UwUFAOTBYwGuAqQBAgIA6LZXAckEFwYLdw02VQKzAr0BAgIAzKpOAbYEMgIC"
	.ascii	"ADF4mAHAA2EEBAAEPFkB1gLbAiwNiwIkdpYAmgR0AwMAFk5rAbwCJQMDAAg5"
	.ascii	"VQGuA08ECWAOMD4AvgLVAQICG7ugWwKrBFwEBAAXYIgBqwJrBQUA7tt2AcQD"
	.ascii	"rgICAlMpXIAC1gKFAQQEAN6uQwHNAn4DAwDQtFABsAOkAQUK4QIhh6QCiAQV"
	.ascii	"BQUAC0NeAeoCdwMDAO/NdwGNBGECAgAoka8BsQL5AQMDAAw4VQHPAs4BBAQA"
	.ascii	"7MZbAcQCPAYGANuuVgHyAroBAgIAzpVRAcQBjgICAgAYaYoBvALVAQICAOPa"
	.ascii	"mwFv2wICAgAVSmsBgQR3AgIAF0xkAZICHwICACRcdgHYA8MBAgIAFHmdAcwD"
	.ascii	"owECAgA0gaMBrwGmAgICAHnY6gFumgIDAwAkXnUBwAONAQQEACRwiwH4Ad0C"
	.ascii	"EwhWQnKJAKcEqgEEBAAvV2UBlQPcAQICAA0qPAHOApwCAgIAKmeDAeUByAEG"
	.ascii	"AtkBM4SnAJMCoAECAgCwkmcBpQPMAgICGkyCowDMBFcSCPABDEtsAt4CuAEG"
	.ascii	"BgDQmT4BrwQlAg2EAgc7VgKlA4IBAgIA2sF5AZQBkwIDA+EBDFdzAmPVAQoK"
	.ascii	"AAMbMgHYApsBAgIA6cRhAZIBkAICAgBv1ekB4wPrAQIW9gEUOEwCuQLXAQIC"
	.ascii	"AMCuegGGAm8FCVcTfqEC4wKbAgICN0GQsgDVBFgJAh4CM04CSTY2DEUEFB8A"
	.ascii	"9gK5AQICALWAMAHdAfgBBQj9/wMihq8C2AO+AgICAAIhOQHXAlwCAgC7nloB"
	.ascii	"jAK8AQMCswHPsmAAgQKWAQMDAAYrSAGBBD8CAgAIP1oBmAKzAggCkAIPUnIA"
	.ascii	"xQP7AQIGiwIzj7MAtAIeBgYABSlBAdQESQICAAg8YgHMAiADE4sCDVBwAMwB"
	.ascii	"lwIDAwAunb8BjATpAQUFAAMWKgH7AZMCAgIAJm+NAbcCWgICANisRAGmAZsC"
	.ascii	"AwMAF2+NAcACWgYGAOC+ZgHdA8kCAwINKEpiAJ8CjAICAgATNEsB3ARPAgIA"
	.ascii	"IGGHAYYEWAICADGMsgHIA8sBAgZRBVV5AOYDRgMD6wEkja0C3gJeAwMA0K9g"
	.ascii	"AYIESAQEABJefAGtBGQCAgAHQl4B1wLUAQMDAM2qYAG5AdABAgLmAlGJowCY"
	.ascii	"AZQCBQIXGGWFAN8BsAIDAwAola8BnwGZAgICADOOsQH7An4CAgCZnnQB5AJJ"
	.ascii	"AwMAHG+bAcACzQIMAm1MxeAC/AN5AgIAN32TAYUCjwICFUYuf5wA5gMiAwWC"
	.ascii	"AiB1lgCGBNUCAgKPAi1BVgKkA2MCAgApco0BvAHOAQICAAsnLwH8AY8BAwMA"
	.ascii	"FS1FAdIBsAICAgA5r8kBsQNNGwKJARJIYgLCAckBAgRLJTFLANgCnQICAgAU"
	.ascii	"JDUBoQRYAgIADEpqAeoCNgYGABZliAGzAcIBAwMAJZ27AbYBlwICBI0CFH+f"
	.ascii	"AIEB0QICAgATOUUBgQQpAgIAQLncAbsCygEEBADlxGQB5QPiAQcHACGMsAHC"
	.ascii	"A5EBEAK+ARYvRgL4AZwCAgK2AofM5gClAusBAgKIAS5iewLKAqsBDwltzpo6"
	.ascii	"Av4CSi0ClgEJRF8A+gGgAgICADF+mQHNAoQBAgIA889uAYcD8QECAgBMzOkB"
	.ascii	"iwRmAgIAGGuNAdQBvwEDAwAgi6gBUbkBAgIABRcoAZoCjQIDAwA5e5cBjgIZ"
	.ascii	"GAYQAyxFAoMBxwECEpECRGR1AoMC/gECAr8BO5u4AswDuAIXArwBEztVALQD"
	.ascii	"nwECAkoseYYCnwNcAgIAOLTQAbcCQAICALCDTQH9A8IBAgZiBkZoAIwEdQQE"
	.ascii	"ABdadAH/A9ECAgIAFztTAZ8BywICAgBUn78BzAQ/BAijAQ1MbgLyAggbBJgB"
	.ascii	"BCc6AJ4CHgQLiQItf54AhAKDAgICABRVdwGzAaoCAgIAIHaOAZAC+gECAgBQ"
	.ascii	"y+UByAGBAgICABhxlwFfzgICAgAFITsBnQK4AQICAObIewHYBE4CAgAEMVAB"
	.ascii	"kAMSBgYACzxTAboDRwcHAAUoPgGwAasCAgIucLLMAuQEKwUFAAo3UwHnAu0B"
	.ascii	"AwMANyQXAaQDswECAgBSiqYB8QHkAQICpwJRt9MA4wJdAgKiAa2kcQCCArMC"
	.ascii	"BQUABhstAd4DKQcHABFigQHrAYACAgIAOJiyAQMQrhP6ApcBCAgA16RBAYAD"
	.ascii	"qgECAgDp05cBmwOtAQULwQEUUG4AhQOyAQYGAN+xSwGsA8wBAgIARZm0AZgE"
	.ascii	"SgICADiFqwG0A50BAgIAFj5JAZAESgUHYglTdgCeA5oBCw1UJUFKAqIETwUF"
	.ascii	"ACFwkwGYAtQBBgYAET9cAeUCbxgCXS9ZYgDTAtoCbwaNAgcrRQDeAqcCRgKS"
	.ascii	"AgclPAKGA6QBBQUA2rhpAaUDxAECAgBFlKsBkQOWAQgIAO3GVwHjAr4BFAL2"
	.ascii	"AVVLRQLQA7kBAgIARqDDAcADxwEHBwAolLYBwwGSAgICAEKszgGDA5oBCAKg"
	.ascii	"Ar+TQgK7AYcCGwQrL42tAv0C4gEEBAAYNEsBjgOJAgMDACtAVQHnArIBBAQA"
	.ascii	"SEhIAZoETwMDAA5FYQGrAtMBCgYj4cKBArUBgwIMApACGWaLAK4B6QECJ1og"
	.ascii	"f54CqQQ1BgKuAUaGqALNAt8BBAQAMTpHAccBuQIFBQAwkbEBigOBAQoKANWj"
	.ascii	"SAGeAsIBBQUA7cpmAWGlAgIJzwEfOUcC+gPRAQMDAA5zmAHpAtoBCAgABDFT"
	.ascii	"AcYC5wEOCIUCDRgmAP4CuAECDoQCDS1CAo8DtAECAgA3QS8BtwHrAQQakAIm"
	.ascii	"kLQAuAKfAgICABJlgQG7AesBAwMAZtLiAZEDsAEEBE8dLzYApwKgAgMDABFV"
	.ascii	"dQGxA5IBAwMAGWyFAdcC4QEEBABKLyQB3ALMAQICALWWPAG9AakCAgIAQpzA"
	.ascii	"Ac0B"
	.ascii	"+wECQ4sCJo2wAvYC5wEEBAAaGyMBxAOuAQICAB55lQHpAo8CAgIAgFFJAccD"
	.ascii	"vAECAr4CXcHXAqcDmQECAgAjXngBpgOSAQICABg+UQGFA70BAgIAESw0AckE"
	.ascii	"owEQEAAFChcBnQLdAQIDmwEbUXkAqgSZAQoKAAUJFAGpA7EBAwMAFGZ+AeIB"
	.ascii	"ggIDAwAlcY8BtAQ5BAQAF1x5AXyhAhYCUxZjhQDRAtoBAgIAUSsbAXtzAhrw"
	.ascii	"ASBYawLsAYoCAgIAmOj1AckD7AEIQVoBEygA4ALLAQICAL6OMQGJAcgCAgKq"
	.ascii	"AlGrwgDcA8YBCAMtF3WTANcBrAICAgAshZwBpgQ+BQUAHHKUAY8DpgECAgDN"
	.ascii	"sDgB0AOqAggDjQIgP1MA5QH/AQICAlSsywC1A5YBAgIAPH2IAawD6QECAgA5"
	.ascii	"kLMBGaECggEIlgIEGCwCqQHuAQQEACGHpgHKAo8BAgt81dBmAvoCrwEDAwDX"
	.ascii	"vFYBpgLUAQICAK6ddQGGA1oJBM8CG3qVAKYDeQICANW8fQG0BAUZBOICDCpC"
	.ascii	"APwCqAECAgCxlFMB8AL0AQMDABoTHgHDAmsCAgDVrTgBjgIvAgIApXA1AakC"
	.ascii	"5AEDAwAPL0MBX7cCAgIAHzZMAdgDuwEDBLACJYajAE2jAQgCxQIzf6AC1AKR"
	.ascii	"AQMDAOPNcQHDA7wBAgIAPLPTAZsDpgECAgBDU14B8QIcBBSkAgpBXQDIAfwB"
	.ascii	"BwIWLpq0AqoDkAEDAwAdaIEB7wKvAQQEANahSQGBA+4BAgIAF2qIAdkDKjgD"
	.ascii	"jwIRWXoAzAKOAQICAPntkwGlAv0BAwMAImCDAesCYwICAL6yfQGjAd8BAgZt"
	.ascii	"KHOLAKgDagICANfKhAHSATgODgADKEABxwPTAQMDABV1lgGaA6IBAgIwqJ6E"
	.ascii	"AtcCbwQEAPPNXgHrAVQCG6oBUbDKAnviARAQAAQiNwHqAYUCAgIAQZi1AbME"
	.ascii	"MwICAAxPbAHGAcEBAgyHAi96lgCPBKMBCAanARVVagC4Am4NArgB5cVzALYB"
	.ascii	"6wECAgBWtcsBwAPLAQIoYhl5mwL3AbwBAgeEAjNAXACuAqcBAgIAt4QsAV29"
	.ascii	"AgICABg3SwHgBEICAgAQW3oBtAK6AQcCBr6SQQCrArABBAQA2p45AboBzQIc"
	.ascii	"JwACIz0AtAHtAQICcRZnfwDEA6cCAwMAIklmAfoDfAYSCAQlPQCUAcYCAwMA"
	.ascii	"Mo+vAbsC4AEDBvsBTyUMAt0B8AECAhE0o8QCogHGAgICAEWduwHuAukBBAQA"
	.ascii	"CiQ7AfsCrQIDAwAzgp0B5wH9AQICABZqhQHOBCICAno8bosA4QHoAQMDABx8"
	.ascii	"nAGLAqYBAge3AdKpWgDuAqYBBAQAyKFPAZcEQAICABNGWgHSBGQEBAAQVnQB"
	.ascii	"lgHnAQICAESDlgHbAcYCBAQABy1DAZ4DzwECAtIBPYidAr0BrQICAgAde6EB"
	.ascii	"iwScAQMDACtlewH8ArQBAgIA3aQ6AZgEfwICABpFWgHfA6wCBgYAFCo1AcQE"
	.ascii	"CgICJ0JlhALwAksOBK4CJFhvAp8C+wECAgAMR2cBpwOEAQICAHGTewHdAb0C"
	.ascii	"BAQAOZi1AcYDrAICAgAONUgB9QK8AQICALN+NgGBApACAgJ6csbbArkEPwMD"
	.ascii	"ABNaeAGtAvIBAwMAGkxmAbQD3wEEBMEBE3acAJAC3QJpDMsCJ4OjAo0CogID"
	.ascii	"AwAFJ0EBvgHQAQICAEeClAHXBL0BAhnKAQUhNgLgAkkCAgAubHgB3AKWAgIE"
	.ascii	"WRUvPABczwEICAAEFy8BwQIqBAQADExrAY4ERQQEAAxBWgHLA5gBBALIAiRf"
	.ascii	"cwK4AbkCAgIAGnWUAZwC+QECAgAue5wBsQPdAQICRVKwzwLNBFACAtwBVsbg"
	.ascii	"AJoExQEEBAAQW3wB3wHtAQ4CByGHqACTAY4CAgIAUcjiAYQCjAICB+QCJnKR"
	.ascii	"ApsCggIDAkwncIgAtALxAQcbsQEELUgA7AJeAgIAKzxCAbMDigEOAgQUaYMC"
	.ascii	"a5wCAgIASW+DAcUB/AECArMCD2WDANgDrgEFBQAgfZ8BwAOPAQICABpfeQH/"
	.ascii	"AnoCAgCjoG8BxwLdAQICADFceQHLBOwBCQeSAQxDZQLcAtIBAgIAvaZvAbAE"
	.ascii	"ZAICAB5zkAHUBCAEBAAPNlEBhwReBQUAHXueAY4D3QEZAtMCG1lxAlFXMAeL"
	.ascii	"AQUXJADJAyYCA84CNp3AAJoBygIDAwA3iKUBqgRsAxUnEzhQANgDuQECAgBt"
	.ascii	"2vEByAQhBxPEAhFKawCWAZcCAgIAC1l1AY8CvAEFBEzoy2YClgR7AgLkAjph"
	.ascii	"dgLEA60CAgLnATlqjwLlAdEBAgIAKZm6AZ0EewMDACBIXwGAAqkBAgIAr5tg"
	.ascii	"AekBxgEKAq8BR46rAPcChQECAgDCrXABmAM9AiH0AQtPbQDLA6ABAgIAK2aN"
	.ascii	"AY8DoAECAgDt0XQBqgJkBQUA8+FqAfkBngICA7MBKniTAr4CmwEFIP8ByJM+"
	.ascii	"AKIDsgECAhp1rMcC1wKZAgICAAgyVQG1AsIBBQUA4MNaAaoD5gECAgAbd5YB"
	.ascii	"AI4COASIAQMNFgDiAl0CAgDkz5QBqQHFAgMDADGTuwEDEd0K/QK+AgICAFGb"
	.ascii	"sAH9Ao8BCgOIAuC1WwDdAZACCgoAMJS1Ac4BhwIDAwAbaoIBrgOgAQMDABU+"
	.ascii	"TgHnAs8BFwRiRDIqAo8C1QEGBgANS2sBlgOZAQcHAO3EVAHIA78BAwxYKKDC"
	.ascii	"AI0D1gIJGQQEIzsAigPZAgICACJBXwGUA4wBBAQA581rAZADhgIKCa4BER4p"
	.ascii	"AGOiAg4JkwIhYX8AlwLNAQICAC1BPwG4AYwCAwMAG2uKAesCxgEDAwAuPlcB"
	.ascii	"qQQ4AgIADVBzAZ4DvAEGBgAXYH0BowOuAQMDABVMZgGUA3gICADgqkEB7gJ8"
	.ascii	"AgIAm5RYAdEDtgECAgAVeJoBlgOqAQIIWxU0QgCfA6EBAwMAKzlCAcYBuwIC"
	.ascii	"AgBDqsgB8QJiAwMADD1XAeoCkgICAgBDMz8BxAH0AQMDAB97nwGHA3sFBQDK"
	.ascii	"l0cBpAKgAhEFpAIedpMArAPLAQIC4QJerMMCrQLWAQICAMuwdQGpA6MBAgIA"
	.ascii	"Cio4AZ0C0wEFD5oCDj9fAMgDwAECAgAjgKEB7AKOAgICADsoIwHwAZwCBQUA"
	.ascii	"JpG4AbkBggICAgAzkq4BzwO4AQICOXHL5gLbAskBAgIA6s1lAYkBlQIDAwAh"
	.ascii	"d6EB+wLqAQMDACM4VQGnAsUBCAgA7M5vAb8DwwEDAwAdhqkB/ALDAgICBBlT"
	.ascii	"bQCCA70BAiQKFTxWAL8DiwJLAgwBEycCsQSLATALiwIDCxgAgAO5AQMDANuu"
	.ascii	"TwH+AqYBAwMAvqNZAfgCjgEFBQDeqkMBnQOoAQICAAsmQgG8AfoBAgKyAk2q"
	.ascii	"xwCsA40BAgIAE150AZQBhQIjAmYmhqUCiAOfAQICAOm9UwHmAaACBAQAJY2s"
	.ascii	"AaoDtQECAgA/nLUBoQSIAR0LWwUIDwLhAUcJCQACJToBxAGSAgICAEi21AG/"
	.ascii	"AacCAgIAIXmYAYMBnQIDAwA4ocAB7QGEAgICAB9+nQHtAxECHFcNVnQAnwRV"
	.ascii	"AgIAFU9sAXvmAQYRuQIGJToAtQLWAQMDANzFkgGFA68BBgYA4LRPAdECHSID"
	.ascii	"uQEGNlMAoQLTAQMCygEuOzUAggOEAgMDAAgdLgHjA8QBAg9aBlZ1Au8BUwUF"
	.ascii	"AEirxQHSAtoBAgIAVjAhAaoDhAECAgAdepMB6wK7AQMDAE1DTQH9A84BAgIA"
	.ascii	"L53GAeUB6AECAgAxl7kBuAQEAhXTAg43UADFA8oBAgIAMqbIAZYETQICAAlD"
	.ascii	"YQGKA5gBAgIA5MR0AeMDsAIDA1MlOEMC0wE6BgYABS1HAYsEngEEEacBFVd0"
	.ascii	"APIDRQQEdxpwlwD9AoMBBQUA0KVLAcEDqQICAgAKJzcBhAOgAQME2gLsxnUA"
	.ascii	"1AOtAgIC1AFGaX4CrgOZAQoC0wIgVmkAjgRNAgIAA1Z9Aa0C9QECAgAuYn0B"
	.ascii	"owPEAQUHWRZxkACmA2cDAwDJs10B+AMtAgIAHnSSAd0BgAICAskBEl13AKcC"
	.ascii	"0gECAgDcunIBnAL2AQMDABtegAHuAe8BAgIAG3GSAaoD6AECAhZQosYCtgHz"
	.ascii	"AQUFACKGpgHmAs8BBwYDBDpeAIYEeAUYjgIEIjkAwASzAQUCPxocGgBtmwIC"
	.ascii	"AgAkWXABmwH7AQICAClxjAHCAuoBAgv9AR8oKgKYAsQBAgOyAs60dwDKAZwC"
	.ascii	"AwMAK52+AaAB4AEFBAodbIQClQGQAgMDAGTY6QHxAm8CAgAxVFYBlQHJAgIC"
	.ascii	"ACOAnwH3A0ACAqEBFE9hAMEB0AECAgBAkqEBowHLAgQEAD6IqAGEA5cBAgKG"
	.ascii	"ArWIRQBPwAIMDAACGS8BtAKeAgUDCwhffAK0AZ8CAgIAPJa4Ab4BywICApwB"
	.ascii	"DD5fAKQDeAICAPbGagEDErsG7wKUARIKqgHUo0IA1gKzAmECjwIFIjkAkwLN"
	.ascii	"AQQEACRFVAHyAnsDAwAoXG4B3QGWAgICAEihwQHxAswBAgIAck1AAZgDfQIC"
	.ascii	"AMaSLAGhA6MBBAQAFCk4AWSkAgICACQ0OwHDAYECBQ2cAiCCqADpAY8CBAQA"
	.ascii	"JY62AYoCzgEEBAAVT3IBnAO4ARUF1QIddJIAxAHvAQICWmW51QCfA6UBFAKQ"
	.ascii	"AR1WbAKKAt4BBQUAHWqKAbUBjQICAgAUWncBpgLYAQICABYtPwHaAswBAgIA"
	.ascii	"tJY4AWStAgICAC5ZagH+ArwCAgKvAjxmfQK5AcICAwMAH4OjAYIDdwICAJuk"
	.ascii	"eAGqA48BAgIALHmTAc4DxwEDAwAwpMcB6wGfAgICZmvL4QDHAb4CAgIAJX6f"
	.ascii	"Ae8CYwICAB1ATQHDAZUCAgIAGKO0AesCygECAgBERVwBngOWAQMDAOq+YQFr"
	.ascii	"nwICC5YCImWDAJUDawcKswHcqz4AlQOAAQICAM6bMgHzAtYBBAOpAlQ/MgKD"
	.ascii	"A9EBAhqQAhMwRQKaA6gBAgIAIjNGAe8BWQQEAE21zgGqA4YCRQnnAgMVKwL0"
	.ascii	"AtsBAgjjAjElIQClAZQCAwMAKo+vAcoDuwEFBK4CHYOlAsUDwAECAgBBqMMB"
	.ascii	"1gGIAgICAEOQqQH7AswBBQUADyhAAaYB9wECAgAhbIQBwwGnAgMDADCRrAF/"
	.ascii	"mwIDAwBGrc0BjQOYAQICAN66SQGrBDUCA5EBQoKkAPkDHwgIAA5TdAGqA7IB"
	.ascii	"AgIAE22FAfgC6AEQArYBIEVjAqUDZgYCmwLRyYEAwgG4AgIGrwEdg6ICtwG9"
	.ascii	"AgICAHzO5AHhAZICAgIARpuvAbICoAICAgAhiaUB/QOYAQIcYBNkhACxAfcB"
	.ascii	"AgIANZ/AAasEOgICABFQcwGwAtQBBAQA4cSCAZYBkwICAgBx198BiAOOAQQE"
	.ascii	"AN6tSgGSBD4hA2ceb5EA6wFRAgIAP4qmAa0CmQICAgAYYogBxwH3AQICAB96"
	.ascii	"nQGiA2sEBADdq0QB/wKoAQICAMW0egGNA48BBQWGAvHOZQDAAdABAgIATpmo"
	.ascii	"AasCzgEDAwDqy38BtQGiAgICACd7nAGKA6oBBAO5AeC6ZAIDE5MD/AKTAhcO"
	.ascii	"ZwIcMgCUAtABBAQACzpWAZQCyAECAgDKwpgB3gGbAgQEACSGpwGmA6gBAgIA"
	.ascii	"O2V6AacDsAE7ApABJoqoAusBjAICAvT/AyNykwDtApIBAgsLqpZYApoDfwIC"
	.ascii	"AOu8UwGmAtUBAgaNAhMqPAC0A6IBAgIAH3SJAYEDngECAgC7lUgBxAGEAgMD"
	.ascii	"AB6VtQGgA5UBAgKuAW1nQAKbA68BAinWARxjgQKsA7MBBAPUARVwjQKFA3kD"
	.ascii	"AwDLmUcB+gHXARgC2AEca4oC7QLIAQICABwvPwGhA5MBAgIA48JwAewBngIC"
	.ascii	"AgArkrYBW6QCCAgABhYsAZsDqgEDAwAJJEABiALfAQICACV+nQG5Ab8CAgIA"
	.ascii	"L42oAcQBqAICAsQBSKfIAocDywICAgAVM0oB6wGUAgICAECTvAG+AcMCBAQA"
	.ascii	"J4irAYIDlQECAgDVpTgBngQ/BwctH3mdAKoDugEDAwAZfpoBzwGGAgICACFw"
	.ascii	"gQGYAZECAgIAcdrnAe0DnwECC5UBE2eFAocDggIIAtEBNWB3AgMUuwGQA7AC"
	.ascii	"CgoABylCAZQCywECAgBJV1UBowOXAQICAD1PRAGVA7EBBg/TARZQbgCWA9UB"
	.ascii	"BAQAE1FzAe8BjgICAgAZdpEBlQLdAQcHAAxJagHGA7IBAgV7KqHDAMUBpgID"
	.ascii	"AwAliKcBjALcAQICADB0lQGBA30DAwDR"
	.string	"nUYB4AGXAgICACSGqQGJAtkBAgIAEFt/AakDqAECAgAWTWYB0AGCAgMDAGje6AHQAYcCAgIACVdnAaIDtwEDAwAYXXkBAhVRkQLNAQQEABg+UwGVA6UCBC61AQcwTQKiA5sBCgMoHUpcAI0DuQECC9gBFUtpAJsDtwECEawBGWiKApMCyAECAgDAupIBwwGoAgICgQFFp8UCAhYjlAOlAhAFwQEQJDsAqgOeAQIC1AE6V24AkwLMAQICABYzSQE="
	.align	2
.LC31:
	.string	"Decoded bytes:"
	.align	2
.LC32:
	.string	"Declaring variables #1"
	.align	2
.LC33:
	.string	"Declaring variables #2"
	.align	2
.LC34:
	.string	"Decoding first varint"
	.align	2
.LC35:
	.string	"Increment"
	.align	2
.LC36:
	.string	"Decoding second varint"
	.align	2
.LC37:
	.string	"Enter loop"
	.align	2
.LC38:
	.string	"header size"
	.align	2
.LC39:
	.string	"Decode varints"
	.align	2
.LC40:
	.string	"Target end cursor calc"
	.align	2
.LC41:
	.string	"Enter loop 2"
	.align	2
.LC42:
	.string	"Cursor, targetEndCursor"
	.align	2
.LC43:
	.string	"Instance"
	.align	2
.LC44:
	.string	"Part"
	.align	2
.LC45:
	.string	"WedgePart"
	.align	2
.LC49:
	.string	"Size"
	.align	2
.LC50:
	.string	"CFrame"
	.align	2
.LC51:
	.string	"Shape"
	.align	2
.LC53:
	.string	"No part created. Shape type: "
	.align	2
.LC54:
	.string	"Material"
	.align	2
.LC56:
	.string	"Anchored"
	.align	2
.LC57:
	.string	"Parent"
	.align	2
.LC58:
	.string	"Color"
	.section	.text.startup,"ax",@progbits
	.align	2
	.globl	main
	.type	main, @function
main:
	lui	a0,%hi(.LC8)
	addi	sp,sp,-544
	addi	a0,a0,%lo(.LC8)
	sw	ra,540(sp)
	sw	s0,536(sp)
	sw	s1,532(sp)
	sw	s2,528(sp)
	sw	s3,524(sp)
	sw	s4,520(sp)
	call	_ZN4Rbxl9getGlobalEPKc
	mv	a1,a0
	addi	a0,sp,116
	call	_ZN6LuaObjC1EPv
	lui	a0,%hi(.LC15)
	addi	a0,a0,%lo(.LC15)
	call	_ZN3Lua5printEPKc
	lui	a0,%hi(.LC16)
	addi	a0,a0,%lo(.LC16)
	call	_ZN3Lua5printEPKc
	lui	a0,%hi(.LC17)
	addi	a0,a0,%lo(.LC17)
	call	_ZN4Rbxl10getServiceEPKc
	mv	a1,a0
	addi	a0,sp,120
	call	_ZN6LuaObjC1EPv
	lui	a1,%hi(.LC18)
	addi	a0,sp,124
	addi	a1,a1,%lo(.LC18)
	call	_ZN6LuaObj10fromStringEPKc
	lui	s1,%hi(.LC19)
	addi	a1,s1,%lo(.LC19)
	addi	a0,sp,128
	call	_ZN6LuaObj10fromStringEPKc
	lui	s0,%hi(.LC20)
	li	a3,131072
	addi	a2,sp,124
	addi	a3,a3,3
	addi	a1,s0,%lo(.LC20)
	addi	a0,sp,120
	call	_ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i
	mv	a1,a0
	addi	a0,sp,132
	call	_ZN6LuaObjC1EPv
	li	a3,131072
	addi	a3,a3,3
	addi	a2,sp,128
	addi	a1,s0,%lo(.LC20)
	addi	a0,sp,132
	call	_ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i
	mv	a1,a0
	addi	a0,sp,136
	call	_ZN6LuaObjC1EPv
	lui	a0,%hi(.LC21)
	addi	a0,a0,%lo(.LC21)
	call	_ZN4Rbxl9getGlobalEPKc
	mv	a1,a0
	addi	a0,sp,432
	call	_ZN6LuaObjC1EPv
	lw	a0,432(sp)
	li	a2,131072
	addi	a2,a2,3
	addi	a1,sp,136
	call	_ZNK6LuaObj4callIS_EEPvRKT_i.isra.0
	mv	a1,a0
	addi	a0,sp,140
	call	_ZN6LuaObjC1EPv
	addi	a0,sp,432
	call	_ZN6LuaObjD1Ev
	lw	a0,140(sp)
	li	a2,0
	addi	a1,s1,%lo(.LC19)
	call	_ZNK6LuaObj16callMethodStaticEPKci.isra.0
	lui	a0,%hi(.LC22)
	addi	a0,a0,%lo(.LC22)
	call	_ZN3Lua5printEPKc
	call	_ZN4Rbxl10getServiceEPKc.constprop.0
	mv	a1,a0
	addi	a0,sp,144
	call	_ZN6LuaObjC1EPv
	lui	a1,%hi(.LC23)
	addi	a0,sp,148
	addi	a1,a1,%lo(.LC23)
	call	_ZN6LuaObj10fromStringEPKc
	li	a3,131072
	addi	a3,a3,3
	addi	a1,s0,%lo(.LC20)
	addi	a2,sp,148
	addi	a0,sp,144
	call	_ZNK6LuaObj10callMethodIS_EEPvPKcRKT_i
	mv	a1,a0
	addi	a0,sp,152
	call	_ZN6LuaObjC1EPv
	lw	a1,152(sp)
	lui	s0,%hi(.LC24)
	addi	a2,s0,%lo(.LC24)
	addi	a0,sp,156
	call	_ZNK6LuaObj17getPropertyObjectEPKc.isra.0
	addi	a0,sp,204
	call	_ZN7Vector3C1Ev
	addi	a0,sp,156
	call	_ZNK6LuaObj6handleEv
	mv	a1,a0
	addi	a0,sp,204
	call	_ZN7Vector314readFromObjectEPv
	lui	a0,%hi(.LC25)
	addi	a0,a0,%lo(.LC25)
	call	_ZN3Lua5printEPKc
	lw	a0,204(sp)
	call	_ZN3Lua5printEf
	lw	a0,208(sp)
	call	_ZN3Lua5printEf
	lw	a0,212(sp)
	call	_ZN3Lua5printEf
	lui	a5,%hi(.LC26)
	flw	fa4,%lo(.LC26)(a5)
	flw	fa5,204(sp)
	addi	a0,sp,204
	fadd.s	fa5,fa5,fa4
	fsw	fa5,204(sp)
	call	_ZNK7Vector38toObjectEv
	mv	a1,a0
	addi	a0,sp,432
	call	_ZN6LuaObjC1EPv
	addi	a1,s0,%lo(.LC24)
	addi	a2,sp,432
	addi	a0,sp,152
	call	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	addi	a0,sp,432
	call	_ZN6LuaObjD1Ev
	lw	a1,152(sp)
	lui	a2,%hi(.LC4)
	addi	a0,sp,160
	addi	a2,a2,%lo(.LC4)
	call	_ZNK6LuaObj9getMethodEPKc.isra.0
	lui	a5,%hi(_Z15touchedCallback6LuaObj)
	lui	a1,%hi(.LC27)
	li	a3,8192
	addi	a2,sp,432
	addi	a5,a5,%lo(_Z15touchedCallback6LuaObj)
	addi	a1,a1,%lo(.LC27)
	addi	a0,sp,160
	sw	a5,432(sp)
	call	_ZNK6LuaObj10callMethodIPvEES1_PKcRKT_i
	lui	a5,%hi(.LC5)
	lw	a1,%lo(.LC5)(a5)
	addi	a0,sp,164
	lui	s0,%hi(.LC35)
	call	_ZN6LuaObj9fromFloatEf
	lui	a5,%hi(.LC28)
	lw	a1,%lo(.LC28)(a5)
	addi	a0,sp,168
	call	_ZN6LuaObj9fromFloatEf
	addi	a0,sp,172
	mv	a1,zero
	call	_ZN6LuaObj9fromFloatEf
	lw	s2,116(sp)
	addi	a1,sp,164
	mv	a0,s2
	call	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.1.isra.0
	addi	a1,sp,168
	mv	a0,s2
	call	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.1.isra.0
	lui	a0,%hi(.LC29)
	addi	a0,a0,%lo(.LC29)
	call	_ZN3Lua5printEPKc
	addi	a1,sp,164
	mv	a0,s2
	call	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.1.isra.0
	addi	a0,sp,216
	call	_ZN6vectorIhEC1Ev
	lui	a0,%hi(.LC30)
	addi	a1,sp,216
	addi	a0,a0,%lo(.LC30)
	call	_Z13base64_decodePKcR6vectorIhE.isra.0
	lui	a0,%hi(.LC31)
	addi	a0,a0,%lo(.LC31)
	call	_ZN3Lua5printEPKc
	lw	a0,220(sp)
	call	_ZNK6vectorIhE4sizeEv.isra.0
	mv	s4,a0
	call	_ZN3Lua5printEi
	lui	a0,%hi(.LC32)
	addi	a0,a0,%lo(.LC32)
	call	_ZN3Lua5printEPKc
	lui	a0,%hi(.LC33)
	addi	a0,a0,%lo(.LC33)
	sw	zero,176(sp)
	call	_ZN3Lua5printEPKc
	lui	a0,%hi(.LC34)
	addi	a0,a0,%lo(.LC34)
	sw	zero,180(sp)
	call	_ZN3Lua5printEPKc
	addi	a2,sp,176
	addi	a1,sp,180
	addi	a0,sp,216
	call	_Z12decodeVarintRK6vectorIhERiPi
	mv	s3,a0
	addi	a0,s0,%lo(.LC35)
	call	_ZN3Lua5printEPKc
	lui	a0,%hi(.LC36)
	addi	a0,a0,%lo(.LC36)
	sw	zero,176(sp)
	call	_ZN3Lua5printEPKc
	addi	a2,sp,176
	addi	a1,sp,180
	addi	a0,sp,216
	call	_Z12decodeVarintRK6vectorIhERiPi
	mv	s1,a0
	addi	a0,s0,%lo(.LC35)
	call	_ZN3Lua5printEPKc
	sw	zero,176(sp)
	call	_ZN4math3radEf.constprop.1
	mv	s0,a0
	call	_ZN4math3sinEf
	call	_ZN4math3radEf.constprop.0
	call	_ZN4math3cosEf
	mv	a3,zero
	mv	a2,s0
	addi	a0,sp,64
	mv	a1,a3
	call	_Z22cframe_fromEulerAnglesfff
	lui	a0,%hi(.LC37)
	addi	a0,a0,%lo(.LC37)
	call	_ZN3Lua5printEPKc
	lw	s0,180(sp)
	bleu	s4,s0,.L180
	fcvt.s.w	fa5,s3
	lui	a5,%hi(.LC46)
	lui	a4,%hi(.LC48)
	fsw	fa5,20(sp)
	fcvt.s.w	fa5,s1
	lw	a3,%lo(.LC48)(a4)
	lw	a4,%lo(.LC48+4)(a4)
	fsw	fa5,32(sp)
	flw	fa5,%lo(.LC46)(a5)
	lui	a5,%hi(.LC55)
	sw	s5,516(sp)
	fsw	fa5,40(sp)
	flw	fa5,%lo(.LC55)(a5)
	lui	a5,%hi(.LC1)
	sw	s6,512(sp)
	fsw	fa5,44(sp)
	flw	fa5,%lo(.LC1)(a5)
	sw	s7,508(sp)
	sw	s8,504(sp)
	sw	s9,500(sp)
	sw	s10,496(sp)
	sw	s11,492(sp)
	sw	a3,24(sp)
	sw	a4,28(sp)
	fsw	fa5,52(sp)
	sw	s2,56(sp)
	sw	s4,60(sp)
.L191:
	lui	a5,%hi(.LC38)
	addi	a0,a5,%lo(.LC38)
	call	_ZN3Lua5printEPKc
	lui	a5,%hi(.LC39)
	addi	a0,a5,%lo(.LC39)
	addi	s0,s0,1
	sw	s0,180(sp)
	call	_ZN3Lua5printEPKc
	addi	a2,sp,176
	addi	a1,sp,180
	addi	a0,sp,216
	call	_Z12decodeVarintRK6vectorIhERiPi
	addi	a2,sp,176
	addi	a1,sp,180
	mv	s11,a0
	addi	a0,sp,216
	sw	zero,176(sp)
	call	_Z12decodeVarintRK6vectorIhERiPi
	lui	a5,%hi(.LC40)
	mv	s10,a0
	addi	a0,a5,%lo(.LC40)
	sw	zero,176(sp)
	call	_ZN3Lua5printEPKc
	lui	a5,%hi(.LC41)
	addi	a0,a5,%lo(.LC41)
	lw	s0,180(sp)
	call	_ZN3Lua5printEPKc
	lui	a5,%hi(.LC42)
	addi	a0,a5,%lo(.LC42)
	call	_ZN3Lua5printEPKc
	mv	a0,s0
	call	_ZN3Lua5printEi
	add	s10,s0,s10
	mv	a0,s10
	call	_ZN3Lua5printEi
	lw	a0,56(sp)
	addi	a1,sp,172
	call	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.1.isra.0
	lui	a5,%hi(.LC43)
	addi	a0,a5,%lo(.LC43)
	call	_ZN4Rbxl9getGlobalEPKc
	mv	a1,a0
	addi	a0,sp,184
	sw	zero,184(sp)
	call	_ZN6LuaObjC1EPv
	lui	a5,%hi(.LC44)
	addi	a1,a5,%lo(.LC44)
	lw	a5,184(sp)
	addi	a0,sp,188
	sw	a5,36(sp)
	call	_ZN6LuaObj10fromStringEPKc
	lui	a5,%hi(.LC45)
	addi	a1,a5,%lo(.LC45)
	addi	a0,sp,192
	call	_ZN6LuaObj10fromStringEPKc
	bge	s0,s10,.L181
	lui	a5,%hi(.LC52)
	flw	fa5,%lo(.LC52)(a5)
	neg	a5,s11
	lw	s1,216(sp)
	fsw	fa5,48(sp)
	sw	a5,16(sp)
	j	.L190
.L182:
	flw	fa3,40(sp)
	fcvt.s.w	fa2,s3
	fcvt.s.w	fa1,s6
	fmadd.s	fa4,fa2,fa3,fa4
	fmadd.s	fa5,fa1,fa3,fa5
.L183:
	flw	ft0,32(sp)
	flw	fa0,20(sp)
	lui	a5,%hi(.LC47)
	fdiv.s	fa5,fa5,ft0
	flw	fa3,%lo(.LC47)(a5)
	lui	a5,%hi(.LC5)
	flw	ft1,%lo(.LC5)(a5)
	lw	a0,16(sp)
	fdiv.s	fa4,fa4,fa0
	fsub.s	fa5,ft1,fa5
	fmul.s	fa5,fa5,fa3
	fsw	fa5,4(sp)
	fdiv.s	fa2,fa2,fa0
	fsub.s	fa4,ft1,fa4
	fmul.s	fa4,fa4,fa3
	fsw	fa4,0(sp)
	fdiv.s	fa1,fa1,ft0
	fmul.s	fa5,fa2,fa3
	fsw	fa5,8(sp)
	fmul.s	fa5,fa1,fa3
	fsw	fa5,12(sp)
	call	__floatsidf
	lw	a2,24(sp)
	lw	a3,28(sp)
	call	__muldf3
	call	__truncdfsf2
	mv	s4,a0
	mv	a0,s2
	call	_ZN3Lua5printEi
	fcvt.s.w	fa5,s2
	fmv.x.s	a0,fa5
	call	_ZN4math3radEf
	mv	s3,a0
	addi	a0,sp,196
	call	_ZN6LuaObjC1Ev
	beq	s11,zero,.L198
	li	a4,1
	beq	s11,a4,.L199
	li	a4,2
	beq	s11,a4,.L200
	lui	a0,%hi(.LC53)
	addi	a0,a0,%lo(.LC53)
	call	_ZN3Lua5printEPKc
	mv	a0,s11
	call	_ZN3Lua5printEi
	li	a5,500
	addi	a0,sp,196
	bgt	s0,a5,.L201
.L189:
	call	_ZN6LuaObjD1Ev
	bge	s0,s10,.L181
.L190:
	addi	a2,sp,176
	addi	a1,sp,180
	addi	a0,sp,216
	call	_Z12decodeVarintRK6vectorIhERiPi
	mv	s5,a0
	addi	a2,sp,176
	addi	a1,sp,180
	addi	a0,sp,216
	sw	zero,176(sp)
	call	_Z12decodeVarintRK6vectorIhERiPi
	mv	s4,a0
	addi	a2,sp,176
	addi	a1,sp,180
	addi	a0,sp,216
	sw	zero,176(sp)
	call	_Z12decodeVarintRK6vectorIhERiPi
	addi	a2,sp,176
	addi	a1,sp,180
	mv	s3,a0
	addi	a0,sp,216
	sw	zero,176(sp)
	call	_Z12decodeVarintRK6vectorIhERiPi
	addi	a2,sp,176
	addi	a1,sp,180
	mv	s6,a0
	addi	a0,sp,216
	sw	zero,176(sp)
	call	_Z12decodeVarintRK6vectorIhERiPi
	lw	s0,180(sp)
	mv	s2,a0
	mv	a0,s1
	mv	a1,s0
	sw	zero,176(sp)
	call	_ZN6vectorIhEixEj.isra.0
	mv	a5,a0
	addi	a1,s0,1
	mv	a0,s1
	lbu	s7,0(a5)
	call	_ZN6vectorIhEixEj.isra.0
	mv	a5,a0
	addi	a1,s0,2
	mv	a0,s1
	lbu	s8,0(a5)
	call	_ZN6vectorIhEixEj.isra.0
	mv	a5,a0
	addi	a1,s0,3
	mv	a0,s1
	lbu	s9,0(a5)
	call	_ZN6vectorIhEixEj.isra.0
	lbu	s11,0(a0)
	addi	s0,s0,4
	sw	s0,180(sp)
	li	a4,1
	fcvt.s.w	fa4,s5
	fcvt.s.w	fa5,s4
	bne	s11,a4,.L182
	slli	s3,s3,1
	fcvt.s.w	fa2,s3
	fmv.s	fa1,fa2
	j	.L183
.L198:
	lw	a0,36(sp)
	addi	a1,sp,188
	addi	s2,sp,288
	call	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.0.isra.0
	mv	a1,a0
	addi	a0,sp,432
	call	_ZN6LuaObjC1EPv
	addi	a1,sp,432
	addi	a0,sp,196
	call	_ZN6LuaObjaSEOS_.isra.0
	addi	a0,sp,432
	call	_ZN6LuaObjD1Ev
	lw	a2,12(sp)
	lw	a1,8(sp)
	mv	a0,s2
	call	_ZN7Vector3C2Efff.constprop.0
	mv	a0,s2
	call	_ZNK7Vector38toObjectEv
	mv	a1,a0
	addi	a0,sp,228
	call	_ZN6LuaObjC1EPv
	lui	a1,%hi(.LC49)
	addi	a2,sp,228
	addi	a0,sp,196
	addi	a1,a1,%lo(.LC49)
	call	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	mv	a3,s3
	mv	a2,zero
	addi	s3,sp,336
	mv	a1,a2
	mv	a0,s3
	call	_Z22cframe_fromEulerAnglesfff
	lw	a2,4(sp)
	lw	a1,0(sp)
	mv	a3,s4
	addi	s4,sp,384
	mv	a0,s4
	call	_ZN6CFrameC1Efff
	mv	a2,s3
	mv	a1,s4
	addi	a0,sp,432
	call	_Z10cframe_mulRK6CFrameS1_
	addi	a0,sp,432
	call	_ZNK6CFrame8toObjectEv
	mv	a1,a0
	addi	a0,sp,240
	call	_ZN6LuaObjC1EPv
	lui	a1,%hi(.LC50)
	addi	a2,sp,240
	addi	a0,sp,196
	addi	a1,a1,%lo(.LC50)
	call	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	addi	a0,sp,240
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,228
	call	_ZN6LuaObjD1Ev
.L185:
	addi	a0,sp,432
	call	_ZN6LuaObj8fromEnumEi.constprop.0
	lui	a1,%hi(.LC54)
	addi	a2,sp,432
	addi	a1,a1,%lo(.LC54)
	addi	a0,sp,196
	call	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	addi	a0,sp,432
	call	_ZN6LuaObjD1Ev
	mv	a0,s2
	call	_ZN6LuaObj8fromBoolEb.constprop.0
	call	_ZN4Rbxl10getServiceEPKc.constprop.0
	mv	a1,a0
	mv	a0,s3
	call	_ZN6LuaObjC1EPv
	flw	fa2,44(sp)
	fcvt.s.w	fa3,s9
	fcvt.s.w	fa4,s8
	fcvt.s.w	fa5,s7
	fdiv.s	fa3,fa3,fa2
	addi	a0,sp,432
	fdiv.s	fa4,fa4,fa2
	fmv.x.s	a3,fa3
	fdiv.s	fa5,fa5,fa2
	fmv.x.s	a2,fa4
	fmv.x.s	a1,fa5
	call	_ZN6Color3C1Efff
	addi	a0,sp,432
	call	_ZNK6Color38toObjectEv
	mv	a1,a0
	mv	a0,s4
	call	_ZN6LuaObjC1EPv
	lui	a1,%hi(.LC56)
	mv	a2,s2
	addi	a0,sp,196
	addi	a1,a1,%lo(.LC56)
	call	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	lui	a1,%hi(.LC57)
	mv	a2,s3
	addi	a0,sp,196
	addi	a1,a1,%lo(.LC57)
	call	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	lui	a1,%hi(.LC58)
	mv	a2,s4
	addi	a1,a1,%lo(.LC58)
	addi	a0,sp,196
	call	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	mv	a0,s4
	call	_ZN6LuaObjD1Ev
	mv	a0,s3
	call	_ZN6LuaObjD1Ev
	mv	a0,s2
	call	_ZN6LuaObjD1Ev
	li	a5,500
	addi	a0,sp,196
	ble	s0,a5,.L189
.L201:
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,192
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,188
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,184
	call	_ZN6LuaObjD1Ev
.L197:
	lw	s5,516(sp)
	lw	s6,512(sp)
	lw	s7,508(sp)
	lw	s8,504(sp)
	lw	s9,500(sp)
	lw	s10,496(sp)
	lw	s11,492(sp)
.L180:
	addi	a0,sp,216
	call	_ZN6vectorIhED1Ev
	addi	a0,sp,172
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,168
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,164
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,160
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,156
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,152
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,148
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,144
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,140
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,136
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,132
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,128
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,124
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,120
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,116
	call	_ZN6LuaObjD1Ev
	lw	ra,540(sp)
	lw	s0,536(sp)
	lw	s1,532(sp)
	lw	s2,528(sp)
	lw	s3,524(sp)
	lw	s4,520(sp)
	li	a0,0
	addi	sp,sp,544
	jr	ra
.L200:
	lw	a0,36(sp)
	addi	a1,sp,192
	call	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.0.isra.0
	mv	a1,a0
	addi	a0,sp,432
	call	_ZN6LuaObjC1EPv
	addi	a1,sp,432
	addi	a0,sp,196
	call	_ZN6LuaObjaSEOS_.isra.0
	addi	a0,sp,432
	call	_ZN6LuaObjD1Ev
	lw	a3,12(sp)
	lw	a2,8(sp)
	lw	a1,52(sp)
.L196:
	addi	a0,sp,228
	call	_ZN7Vector3C1Efff
	addi	a0,sp,228
	call	_ZNK7Vector38toObjectEv
	mv	a1,a0
	addi	a0,sp,200
	call	_ZN6LuaObjC1EPv
	lui	a1,%hi(.LC49)
	addi	a2,sp,200
	addi	a0,sp,196
	addi	a1,a1,%lo(.LC49)
	call	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	lw	a2,4(sp)
	lw	a1,0(sp)
	mv	a3,s4
	addi	a0,sp,240
	call	_ZN6CFrameC1Efff
	call	_ZN4math3radEf.constprop.1
	mv	s2,a0
	call	_ZN4math3radEf.constprop.0
	mv	a2,s2
	addi	s2,sp,288
	mv	a3,a0
	mv	a1,zero
	mv	a0,s2
	call	_Z22cframe_fromEulerAnglesfff
	mv	a3,zero
	mv	a1,s3
	addi	s3,sp,336
	mv	a2,a3
	mv	a0,s3
	call	_Z22cframe_fromEulerAnglesfff
	mv	a2,s3
	mv	a1,s2
	addi	a0,sp,432
	call	_Z10cframe_mulRK6CFrameS1_
	addi	s4,sp,384
	addi	a2,sp,432
	addi	a1,sp,240
	mv	a0,s4
	call	_Z10cframe_mulRK6CFrameS1_
	mv	a0,s4
	call	_ZNK6CFrame8toObjectEv
	mv	a1,a0
	addi	a0,sp,432
	call	_ZN6LuaObjC1EPv
	lui	a1,%hi(.LC50)
	addi	a2,sp,432
	addi	a0,sp,196
	addi	a1,a1,%lo(.LC50)
	call	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	addi	a0,sp,432
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,200
	call	_ZN6LuaObjD1Ev
	j	.L185
.L199:
	lw	a0,36(sp)
	addi	a1,sp,188
	call	_ZNK6LuaObj16callMethodStaticIS_EEPvPKcRKT_i.constprop.0.isra.0
	mv	a1,a0
	addi	a0,sp,432
	call	_ZN6LuaObjC1EPv
	addi	a1,sp,432
	addi	a0,sp,196
	call	_ZN6LuaObjaSEOS_.isra.0
	addi	a0,sp,432
	call	_ZN6LuaObjD1Ev
	li	a1,4096
	addi	a0,sp,432
	addi	a1,a1,-2021
	call	_ZN6LuaObj8fromEnumEi
	lui	a1,%hi(.LC51)
	addi	a2,sp,432
	addi	a1,a1,%lo(.LC51)
	addi	a0,sp,196
	call	_ZNK6LuaObj17setPropertyObjectEPKcRKS_
	addi	a0,sp,432
	call	_ZN6LuaObjD1Ev
	lw	a3,12(sp)
	lw	a2,8(sp)
	lw	a1,48(sp)
	j	.L196
.L181:
	addi	a0,sp,192
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,188
	call	_ZN6LuaObjD1Ev
	addi	a0,sp,184
	call	_ZN6LuaObjD1Ev
	lw	a5,60(sp)
	bgtu	a5,s0,.L191
	j	.L197
	.size	main, .-main
	.weak	_ZGVZ13base64_decodePKcR6vectorIhEE11encodingSvc
	.section	.sbss._ZGVZ13base64_decodePKcR6vectorIhEE11encodingSvc,"awG",@nobits,_ZGVZ13base64_decodePKcR6vectorIhEE11encodingSvc,comdat
	.align	3
	.type	_ZGVZ13base64_decodePKcR6vectorIhEE11encodingSvc, @object
	.size	_ZGVZ13base64_decodePKcR6vectorIhEE11encodingSvc, 8
_ZGVZ13base64_decodePKcR6vectorIhEE11encodingSvc:
	.zero	8
	.weak	_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc
	.section	.sbss._ZZ13base64_decodePKcR6vectorIhEE11encodingSvc,"awG",@nobits,_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc,comdat
	.align	2
	.type	_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc, @object
	.size	_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc, 4
_ZZ13base64_decodePKcR6vectorIhEE11encodingSvc:
	.zero	4
	.hidden	__dso_handle
	.globl	__dso_handle
	.section	.srodata.cst4,"aM",@progbits,4
	.align	2
.LC1:
	.word	981668463
	.align	2
.LC2:
	.word	1127481344
	.align	2
.LC3:
	.word	1119092736
	.align	2
.LC5:
	.word	1065353216
	.align	2
.LC26:
	.word	1084227584
	.align	2
.LC28:
	.word	1073741824
	.align	2
.LC46:
	.word	1056964608
	.align	2
.LC47:
	.word	1092616192
	.section	.srodata.cst8,"aM",@progbits,8
	.align	3
.LC48:
	.word	1202590843
	.word	1065646817
	.section	.srodata.cst4
	.align	2
.LC52:
	.word	953267991
	.align	2
.LC55:
	.word	1132396544
	.section	.sbss,"aw",@nobits
	.align	2
	.type	__dso_handle, @object
	.size	__dso_handle, 4
__dso_handle:
	.zero	4
	.globl	__truncdfsf2
	.globl	__muldf3
	.globl	__floatsidf
	.ident	"GCC: (xPack GNU RISC-V Embedded GCC x86_64) 15.2.0"
	.section	.note.GNU-stack,"",@progbits
