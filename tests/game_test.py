from unittest import TestCase, main

from game_logic import Game, Warrior


class GameTest(TestCase):
    global g
    g = Game("Arrange", 10, {})

    def test_add(self):
        warrior_m_1 = Warrior("M", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
        warrior_m_2 = Warrior("M", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
        warrior_m_3 = Warrior("M", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
        warrior_m_4 = Warrior("M", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
        warrior_w_1 = Warrior("W", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
        warrior_w_2 = Warrior("W", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
        warrior_w_3 = Warrior("W", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)
        warrior_w_4 = Warrior("W", 10, 1, Warrior.DAMAGE_FIELD_M_PAL)

        # Добавляем первого воина-мужчину на клетку (0, 0).
        g.add(0, 0, warrior_m_1)
        self.assertEqual(1, g.get_count_warriors("M"))
        self.assertEqual(0, g.get_count_warriors("W"))

        # Добавляем первого воина-женщину на клетку (7, 0).
        g.add(7, 0, warrior_w_1)
        self.assertEqual(1, g.get_count_warriors("M"))
        self.assertEqual(1, g.get_count_warriors("W"))

        # Пытаемся добавить воина-мужчину на уже занятую клетку (0, 0).
        g.add(0, 0, warrior_m_2)
        self.assertEqual(1, g.get_count_warriors("M"))
        self.assertEqual(1, g.get_count_warriors("W"))

        # Пытаемся добавить воина-мужчину на несуществующую клетку (100, 100).
        g.add(100, 100, warrior_m_3)
        self.assertEqual(1, g.get_count_warriors("M"))
        self.assertEqual(1, g.get_count_warriors("W"))

        # Пытаемся добавить воина-мужчину на несуществующую клетку (100, 100).
        g.add(-1, 5, warrior_m_3)
        self.assertEqual(1, g.get_count_warriors("M"))
        self.assertEqual(1, g.get_count_warriors("W"))

        # Добавляем двух воинов-женщин на существующие незанятые клетки.
        g.add(7, 1, warrior_w_2)
        g.add(7, 2, warrior_w_3)
        self.assertEqual(1, g.get_count_warriors("M"))
        self.assertEqual(3, g.get_count_warriors("W"))

        # Пытаемся добавить лишнюю (четвёртую) воина-женщину.
        g.add(7, 3, warrior_w_4)
        self.assertEqual(1, g.get_count_warriors("M"))
        self.assertEqual(3, g.get_count_warriors("W"))

        # Добавляем двух воинов-мужчин на существующие незанятые клетки.
        g.add(0, 1, warrior_m_2)
        g.add(0, 2, warrior_m_3)
        self.assertEqual(3, g.get_count_warriors("M"))
        self.assertEqual(3, g.get_count_warriors("W"))

        # Пытаемся добавить лишнего (четвёртого) воина-мужчину.
        g.add(0, 3, warrior_m_4)
        self.assertEqual(3, g.get_count_warriors("M"))
        self.assertEqual(3, g.get_count_warriors("W"))

    def test_go(self):
        g.start("M")
        self.assertEqual("Turn M", g.mode)

        g.go(0, 0, 6, 0)
        self.assertEqual(4, g.move_points)
        self.assertTrue((6, 0) in g.warriors)

        g.attack(6, 0)
        self.assertEqual(10, g.warriors[(6, 0)].health)
        self.assertEqual(4, g.warriors[(7, 0)].health)
        self.assertEqual(6, g.warriors[(7, 1)].health)
        self.assertEqual(10, g.warriors[(7, 2)].health)

        g.end_turn()
        self.assertEqual("Turn W", g.mode)

        g.attack(7, 0)
        self.assertEqual(4, g.warriors[(6, 0)].health)
        self.assertEqual(4, g.warriors[(7, 0)].health)
        self.assertEqual(6, g.warriors[(7, 1)].health)
        self.assertEqual(10, g.warriors[(7, 2)].health)


if __name__ == "__main__":
    main()
