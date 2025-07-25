import asyncio
import signal
import tornado.ioloop
import tornado.platform.asyncio
from pyrogram import Client
from py_tgcalls import GroupCallFactory
from PyroUbot import bot, Ubot, get_userbots, remove_ubot, bash, loadPlugins, installPeer, expiredUserbots

async def shutdown(sig, loop):
    print(f"Received exit signal {sig.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [t.cancel() for t in tasks]
    print("Cancelling outstanding tasks...")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def main():
    await bot.start()
    for ub in await get_userbots():
        u = Ubot(**ub)
        try:
            await asyncio.wait_for(u.start(), timeout=10)
        except asyncio.TimeoutError:
            await remove_ubot(int(ub["name"]))
            print(f"[INFO] {ub['name']} tidak merespon (timeout)")
        except Exception as e:
            await remove_ubot(int(ub["name"]))
            print(f"[INFO] error memulai {ub['name']}: {e}")

    await bash("rm -rf *session*")
    await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots())

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))
        except NotImplementedError:
            pass

    await stop_event.wait()
    await bot.stop()

if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    loop.run_until_complete(main())