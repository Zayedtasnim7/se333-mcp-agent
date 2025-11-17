package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CalcTest {

    @Test
    void add_basic() {
        // arrange
        Calc c = new Calc();

        // act
        int result = c.add(1, 2);

        // assert
        assertEquals(3, result);
    }

    @Test
    void add_with_zero() {
        Calc c = new Calc();
        assertEquals(5, c.add(5, 0));
        assertEquals(5, c.add(0, 5));
    }

    @Test
    void add_with_negative() {
        Calc c = new Calc();
        assertEquals(-1, c.add(2, -3));
        assertEquals(-5, c.add(-2, -3));
    }

    @Test
    void add_large_numbers() {
        Calc c = new Calc();
        // 1_000_000_000 + 1_000_000_000 = 2_000_000_000 (within int range)
        assertEquals(2000000000, c.add(1000000000, 1000000000));
    }

    @Test
    void add_commutative() {
        Calc c = new Calc();
        assertEquals(c.add(7, 8), c.add(8, 7));
    }
}
