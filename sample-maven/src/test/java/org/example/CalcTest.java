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
}
