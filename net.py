BUFFER_SIZE = 4


async def write_message(writer, msg: bytes) -> None:
    writer.write(str(len(msg)).encode().ljust(BUFFER_SIZE) + msg)
    await writer.drain()


async def read_message(reader) -> bytes:
    buf = await reader.read(BUFFER_SIZE)
    msg_data = await reader.read(int(buf) + BUFFER_SIZE)

    while len(msg_data) != int(buf):
        buf = msg_data[int(buf):]
        msg_data = await reader.read(int(buf) + BUFFER_SIZE)

    return msg_data
