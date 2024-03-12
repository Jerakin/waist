import pytest

from waist import API, APIError


def test_defined_last():
    api = API("2.0.0")

    class Example:
        @api("==1.0.0")
        def call(self):
            return 1

        @api("==2.0.0")
        def call(self):
            return 2
    e = Example()
    assert e.call() == 2


def test_defined_first():
    api = API("2.0.0")

    class Example:
        @api("==1.0.0")
        def call(self):
            return 1

        @api("==2.0.0")
        def call(self):
            return 2
    e = Example()
    assert e.call() == 2


def test_no_version():
    api = API("3.0.0")

    class Example:
        @api("==1.0.0")
        def call(self):
            return 1

        @api("==2.0.0")
        def call(self):
            return 2
    e = Example()
    with pytest.raises(APIError):
        e.call()


def test_register_twice():
    api = API("3.0.0")

    with pytest.raises(APIError):
        class Example:
            @api("==1.0.0")
            def call(self):
                return 1

            @api("==2.0.0")
            def call(self):
                return 2

            @api("==2.0.0")
            def call(self):
                return 2


def test_multi_function():
    api = API("1.0.0")

    class Example:
        @api("==1.0.0")
        def call(self):
            return 1

        @api("==1.0.0")
        def call_b(self):
            return 3

    e = Example()
    assert e.call() == 1
    assert e.call_b() == 3


def test_outside_of_class():
    api = API("2.0.0")

    @api("==1.0.0")
    def call():
        return 1

    @api("==2.0.0")
    def call():
        return 2

    @api("==1.0.0")
    def call_b():
        return 3

    @api("==2.0.0")
    def call_b():
        return 4

    assert call() == 2
    assert call_b() == 4


def test_():
    api = API("2.0.0")

    @api("<2")
    def call():
        return 1

    @api("<3")
    def call():
        return 2

    @api("<4")
    def call():
        return 3

    assert call() == 3


def test_arguments():
    api = API("2.0.0")

    @api("==1.0.0")
    def call(arg_1):
        return 1 + arg_1

    @api("==2.0.0")
    def call(arg_1):
        return 2 + arg_1

    @api("==1.0.0")
    def call_b(arg_1):
        return 3 + arg_1

    @api("==2.0.0")
    def call_b(arg_1):
        return 4 + arg_1

    assert call(2) == 4
    assert call_b(2) == 6


def test_api_generic():
    api = API("3.0.0")

    @api("==1.0.0")
    def call(arg_1):
        return 1 + arg_1

    @api("==2.0.0")
    def call(arg_1):
        return 2 + arg_1

    @api()
    def call(arg_1):
        return 3 + arg_1
    assert call(2) == 5


def test_api_best_match_prefer_recent():
    api = API("2.1.1")

    @api(">=2")
    def call():
        return 1

    @api(">=2.1")
    def call():
        return 2

    assert call() == 2


def test_api_best_match_prefer_exact():
    api = API("2.1.1")

    @api("==2.1.1")
    def call_b():
        return 3

    @api(">2.1")
    def call_b():
        return 4

    assert call_b() == 3


def test_api_best_match():
    api = API("2.1.0")

    @api("<2")
    def call():
        return 1

    @api("==2.1.1")
    def call():
        return 2

    @api()
    def call():
        return 3

    assert call() == 3
