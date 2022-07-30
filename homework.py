class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        message = (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(self.__class__.__name__,
                                    self.duration,
                                    self.get_distance(),
                                    self.get_mean_speed(),
                                    self.get_spent_calories()
                                    )
        return training_info


class Running(Training):
    """Тренировка: бег."""

    CALORIES_RUN_COEFF_1: int = 18
    CALORIES_RUN_COEFF_2: int = 20

    def get_spent_calories(self) -> float:
        spent_calories = (
                (self.CALORIES_RUN_COEFF_1 * self.get_mean_speed()
                 - self.CALORIES_RUN_COEFF_2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H
        )
        return spent_calories

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WLK_COEFF_1: float = 0.035
    CALORIES_WLK_COEFF_2: float = 0.029
    CALORIES_WLK_COEFF_3: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        spent_calories = (
                (self.CALORIES_WLK_COEFF_1 * self.weight
                 + (self.get_mean_speed()**self.CALORIES_WLK_COEFF_3
                    // self.height) * self.CALORIES_WLK_COEFF_2 * self.weight)
                * self.duration * self.MIN_IN_H
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_SWM_COEFF_1: float = 1.1
    CALORIES_WLK_COEFF_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (
                self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = (
                (self.get_mean_speed() + self.CALORIES_SWM_COEFF_1)
                * self.CALORIES_WLK_COEFF_2 * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_code = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_code[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
