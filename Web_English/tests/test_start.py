import socket

from start import port_is_in_use


def test_port_is_in_use_detects_a_listening_process():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        host, port = listener.getsockname()
        assert port_is_in_use(host, port) is True

