main:
        li      a1, 1
        blez    a0, .LBB0_3
        li      a2, 1
.LBB0_2:
        mv      a3, a2
        mv      a2, a1
        addi    a0, a0, -1
        add     a1, a1, a3
        bnez    a0, .LBB0_2
.LBB0_3:
        mv      a0, a1
        ret