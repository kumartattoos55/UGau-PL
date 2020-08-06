#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import aria2p
import asyncio
import os
from tobrot.helper_funcs.upload_to_tg import upload_to_tg, upload_to_gdrive
from tobrot.helper_funcs.create_compressed_archive import create_archive, unzip_me, unrar_me, untar_me
from tobrot.helper_funcs.extract_link_from_message import extract_link

from tobrot import (
    ARIA_TWO_STARTED_PORT,
    MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START,
    AUTH_CHANNEL,
    DOWNLOAD_LOCATION,
    EDIT_SLEEP_TIME_OUT,
    CUSTOM_FILE_NAME
)
from pyrogram import (
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	Message
)

async def aria_start():
    aria2_daemon_start_cmd = []
    # start the daemon, aria2c command
    aria2_daemon_start_cmd.append("aria2c")
    # aria2_daemon_start_cmd.append("--allow-overwrite=true")
    aria2_daemon_start_cmd.append("--daemon=true")
    # aria2_daemon_start_cmd.append(f"--dir={DOWNLOAD_LOCATION}")
    # TODO: this does not work, need to investigate this.
    # but for now, https://t.me/TrollVoiceBot?start=858
    aria2_daemon_start_cmd.append("--enable-rpc=true")
    aria2_daemon_start_cmd.append("--bt-detach-seed-only=true")
    aria2_daemon_start_cmd.append("--peer-id-prefix=-TR2610-")
    aria2_daemon_start_cmd.append("--user-agent=Transmission/2.61 (13407)")
    aria2_daemon_start_cmd.append("--rpc-allow-origin-all=true")
    aria2_daemon_start_cmd.append("--max-connection-per-server=16")
    aria2_daemon_start_cmd.append("--min-split-size=10M")
    aria2_daemon_start_cmd.append("--rpc-listen-all=true")
    aria2_daemon_start_cmd.append(f"--rpc-listen-port={ARIA_TWO_STARTED_PORT}")
    aria2_daemon_start_cmd.append("--rpc-max-request-size=1024M")
    aria2_daemon_start_cmd.append("--seed-ratio=1.0")
    aria2_daemon_start_cmd.append("--seed-time=0.5")
    aria2_daemon_start_cmd.append("--split=16")
    aria2_daemon_start_cmd.append("--uri-selector=adaptive")
    aria2_daemon_start_cmd.append("--file-allocation=falloc")
    aria2_daemon_start_cmd.append(f"--bt-stop-timeout={MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START}")
    aria2_daemon_start_cmd.append("--follow-torrent=mem")
    aria2_daemon_start_cmd.append("--bt-tracker=udp://tracker.coppersurfer.tk:6969/announce,udp://tracker.opentrackr.org:1337/announce,http://tracker.opentrackr.org:1337/announce,udp://tracker.leechers-paradise.org:6969/announce,udp://9.rarbg.to:2710/announce,udp://tracker.internetwarriors.net:1337/announce,udp://9.rarbg.me:2710/announce,udp://p4p.arenabg.com:1337/announce,http://p4p.arenabg.com:1337/announce,udp://exodus.desync.com:6969/announce,udp://tracker.cyberia.is:6969/announce,udp://retracker.lanta-net.ru:2710/announce,udp://open.stealth.si:80/announce,udp://tracker.tiny-vps.com:6969/announce,udp://tracker.torrent.eu.org:451/announce,http://tracker4.itzmx.com:2710/announce,udp://tracker3.itzmx.com:6961/announce,http://tracker3.itzmx.com:6961/announce,http://tracker1.itzmx.com:8080/announce,udp://tracker.moeking.me:6969/announce,udp://ipv4.tracker.harry.lu:80/announce,udp://bt2.archive.org:6969/announce,udp://bt1.archive.org:6969/announce,udp://explodie.org:6969/announce,http://explodie.org:6969/announce,udp://zephir.monocul.us:6969/announce,udp://valakas.rollo.dnsabr.com:2710/announce,udp://tracker.zerobytes.xyz:1337/announce,udp://tracker.uw0.xyz:6969/announce,udp://tracker.lelux.fi:6969/announce,udp://tracker.kamigami.org:2710/announce,udp://tracker.ds.is:6969/announce,udp://tracker.army:6969/announce,udp://tracker-udp.gbitt.info:80/announce,udp://retracker.akado-ural.ru:80/announce,udp://opentracker.i2p.rocks:6969/announce,udp://opentor.org:2710/announce,udp://chihaya.de:6969/announce,udp://aaa.army:8866/announce,https://tracker.lelux.fi:443/announce,https://aaa.army:8866/announce,http://vps02.net.orel.ru:80/announce,http://tracker.zerobytes.xyz:1337/announce,http://tracker.nyap2p.com:8080/announce,http://tracker.lelux.fi:80/announce,http://tracker.kamigami.org:2710/announce,http://tracker.gbitt.info:80/announce,http://opentracker.i2p.rocks:6969/announce,http://h4.trakx.nibba.trade:80/announce,http://aaa.army:8866/announce,udp://u.wwwww.wtf:1/announce,udp://tracker.jae.moe:6969/announce,udp://t3.leech.ie:1337/announce,udp://t2.leech.ie:1337/announce,udp://t1.leech.ie:1337/announce,udp://retracker.sevstar.net:2710/announce,https://w.wwwww.wtf:443/announce,https://tracker.jae.moe:443/announce,http://tracker.bt4g.com:2095/announce,http://t3.leech.ie:80/announce,http://t2.leech.ie:80/announce,http://t1.leech.ie:80/announce,http://t.overflow.biz:6969/announce,http://retracker.sevstar.net:2710/announce,udp://tracker.yoshi210.com:6969/announce,udp://tracker.teambelgium.net:6969/announce,udp://tracker.skyts.net:6969/announce,udp://tracker.dler.org:6969/announce,udp://tr2.ysagin.top:2710/announce,udp://retracker.netbynet.ru:2710/announce,https://tracker.vectahosting.eu:2053/announce,https://tracker.tamersunion.org:443/announce,https://tracker.sloppyta.co:443/announce,https://tracker.nitrix.me:443/announce,https://tracker.nanoha.org:443/announce,https://tracker.imgoingto.icu:443/announce,https://tracker.hama3.net:443/announce,https://tracker.coalition.space:443/announce,https://tr.ready4.icu:443/announce,https://1337.abcvg.info:443/announce,http://tracker2.dler.org:80/announce,http://tracker.yoshi210.com:6969/announce,http://tracker.skyts.net:6969/announce,http://tracker.dler.org:6969/announce,http://t.nyaatracker.com:80/announce,http://mail2.zelenaya.net:80/announce,udp://tracker6.dler.org:2710/announce,udp://tracker4.itzmx.com:2710/announce,udp://tracker2.itzmx.com:6961/announce,udp://tracker.filemail.com:6969/announce,udp://tr.bangumi.moe:6969/announce,udp://qg.lorzl.gq:2710/announce,udp://bt2.54new.com:8080/announce,http://www.loushao.net:8080/announce,http://trun.tom.ru:80/announce,http://tracker2.itzmx.com:6961/announce,http://t.acg.rip:6699/announce,http://open.acgnxtracker.com:80/announce,")
    #
    LOGGER.info(aria2_daemon_start_cmd)
    #
    process = await asyncio.create_subprocess_exec(
        *aria2_daemon_start_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    LOGGER.info(stdout)
    LOGGER.info(stderr)
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=ARIA_TWO_STARTED_PORT,
            secret=""
        )
    )
    return aria2


def add_magnet(aria_instance, magnetic_link, c_file_name):
    options = None
    # if c_file_name is not None:
    #     options = {
    #         "dir": c_file_name
    #     }
    try:
        download = aria_instance.add_magnet(
            magnetic_link,
            options=options
        )
    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
    else:
        return True, "" + download.gid + ""


def add_torrent(aria_instance, torrent_file_path):
    if torrent_file_path is None:
        return False, "**FAILED** \n" + str(e) + " \nsomething wrongings when trying to add <u>TORRENT</u> file"
    if os.path.exists(torrent_file_path):
        # Add Torrent Into Queue
        try:
            download = aria_instance.add_torrent(
                torrent_file_path,
                uris=None,
                options=None,
                position=None
            )
        except Exception as e:
            return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
        else:
            return True, "" + download.gid + ""
    else:
        return False, "**FAILED** \n" + str(e) + " \nPlease try other sources to get workable link"


def add_url(aria_instance, text_url, c_file_name):
    options = None
    # if c_file_name is not None:
    #     options = {
    #         "dir": c_file_name
    #     }
    uris = [text_url]
    # Add URL Into Queue
    try:
        download = aria_instance.add_uris(
            uris,
            options=options
        )
    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
    else:
        return True, "" + download.gid + ""


async def call_apropriate_function(
    aria_instance,
    incoming_link,
    c_file_name,
    sent_message_to_update_tg_p,
    is_zip,
    cstom_file_name,
    is_unzip,
    is_unrar,
    is_untar,
    user_message
):
    if incoming_link.lower().startswith("magnet:"):
        sagtus, err_message = add_magnet(aria_instance, incoming_link, c_file_name)
    elif incoming_link.lower().endswith(".torrent"):
        sagtus, err_message = add_torrent(aria_instance, incoming_link)
    else:
        sagtus, err_message = add_url(aria_instance, incoming_link, c_file_name)
    if not sagtus:
        return sagtus, err_message
    LOGGER.info(err_message)
    # https://stackoverflow.com/a/58213653/4723940
    await check_progress_for_dl(
        aria_instance,
        err_message,
        sent_message_to_update_tg_p,
        None
    )
    if incoming_link.startswith("magnet:"):
        #
        err_message = await check_metadata(aria_instance, err_message)
        #
        await asyncio.sleep(1)
        if err_message is not None:
            await check_progress_for_dl(
                aria_instance,
                err_message,
                sent_message_to_update_tg_p,
                None
            )
        else:
            return False, "can't get metadata \n\n#stopped"
    await asyncio.sleep(1)
    file = aria_instance.get_download(err_message)
    to_upload_file = file.name
    #
    if is_zip:
        # first check if current free space allows this
        # ref: https://github.com/out386/aria-telegram-mirror-bot/blob/master/src/download_tools/aria-tools.ts#L194
        # archive the contents
        check_if_file = await create_archive(to_upload_file)
        if check_if_file is not None:
            to_upload_file = check_if_file
    #
    if is_unzip:
        check_ifi_file = await unzip_me(to_upload_file)
        if check_ifi_file is not None:
            to_upload_file = check_ifi_file
    #
    if is_unrar:
        check_ife_file = await unrar_me(to_upload_file)
        if check_ife_file is not None:
            to_upload_file = check_ife_file
    #
    if is_untar:
        check_ify_file = await untar_me(to_upload_file)
        if check_ify_file is not None:
            to_upload_file = check_ify_file
    #
    if to_upload_file:
        if CUSTOM_FILE_NAME:
            os.rename(to_upload_file, f"{CUSTOM_FILE_NAME}{to_upload_file}")
            to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
        else:
            to_upload_file = to_upload_file

    if cstom_file_name:
        os.rename(to_upload_file, cstom_file_name)
        to_upload_file = cstom_file_name
    else:
        to_upload_file = to_upload_file
    #
    response = {}
    LOGGER.info(response)
    user_id = user_message.from_user.id
    print(user_id)
    final_response = await upload_to_tg(
        sent_message_to_update_tg_p,
        to_upload_file,
        user_id,
        response
    )
    LOGGER.info(final_response)
    try:
        message_to_send = ""
        for key_f_res_se in final_response:
            local_file_name = key_f_res_se
            message_id = final_response[key_f_res_se]
            channel_id = str(sent_message_to_update_tg_p.chat.id)[4:]
            private_link = f"https://t.me/c/{channel_id}/{message_id}"
            message_to_send += "🌹 <a href='"
            message_to_send += private_link
            message_to_send += "'>"
            message_to_send += local_file_name
            message_to_send += "</a>"
            message_to_send += "\n"
        if message_to_send != "":
            mention_req_user = f"<a href='tg://user?id={user_id}'>Your Requested Files</a>\n\n"
            message_to_send = mention_req_user + message_to_send
            message_to_send = message_to_send + "\n\n" + "#uploads"
        else:
            message_to_send = "<i>FAILED</i> to upload files. 😞😞"
        await user_message.reply_text(
            text=message_to_send,
            quote=True,
            disable_web_page_preview=True
        )
    except:
        pass
    return True, None
#

async def call_apropriate_function_g(
    aria_instance,
    incoming_link,
    c_file_name,
    sent_message_to_update_tg_p,
    is_zip,
    cstom_file_name,
    is_unzip,
    is_unrar,
    is_untar,
    user_message
):
    if incoming_link.lower().startswith("magnet:"):
        sagtus, err_message = add_magnet(aria_instance, incoming_link, c_file_name)
    elif incoming_link.lower().endswith(".torrent"):
        sagtus, err_message = add_torrent(aria_instance, incoming_link)
    else:
        sagtus, err_message = add_url(aria_instance, incoming_link, c_file_name)
    if not sagtus:
        return sagtus, err_message
    LOGGER.info(err_message)
    # https://stackoverflow.com/a/58213653/4723940
    await check_progress_for_dl(
        aria_instance,
        err_message,
        sent_message_to_update_tg_p,
        None
    )
    if incoming_link.startswith("magnet:"):
        #
        err_message = await check_metadata(aria_instance, err_message)
        #
        await asyncio.sleep(1)
        if err_message is not None:
            await check_progress_for_dl(
                aria_instance,
                err_message,
                sent_message_to_update_tg_p,
                None
            )
        else:
            return False, "can't get metadata \n\n#stopped"
    await asyncio.sleep(1)
    file = aria_instance.get_download(err_message)
    to_upload_file = file.name
    #
    if is_zip:
        # first check if current free space allows this
        # ref: https://github.com/out386/aria-telegram-mirror-bot/blob/master/src/download_tools/aria-tools.ts#L194
        # archive the contents
        check_if_file = await create_archive(to_upload_file)
        if check_if_file is not None:
            to_upload_file = check_if_file
    #
    if is_unzip:
        check_ifi_file = await unzip_me(to_upload_file)
        if check_ifi_file is not None:
            to_upload_file = check_ifi_file
    #
    if is_unrar:
        check_ife_file = await unrar_me(to_upload_file)
        if check_ife_file is not None:
            to_upload_file = check_ife_file
    #
    if is_untar:
        check_ify_file = await untar_me(to_upload_file)
        if check_ify_file is not None:
            to_upload_file = check_ify_file
    #
    if to_upload_file:
        if CUSTOM_FILE_NAME:
            os.rename(to_upload_file, f"{CUSTOM_FILE_NAME}{to_upload_file}")
            to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
        else:
            to_upload_file = to_upload_file

    if cstom_file_name:
        os.rename(to_upload_file, cstom_file_name)
        to_upload_file = cstom_file_name
    else:
        to_upload_file = to_upload_file
    #
    response = {}
    LOGGER.info(response)
    user_id = user_message.from_user.id
    print(user_id)
    final_response = await upload_to_gdrive(
        to_upload_file,
        sent_message_to_update_tg_p,
        user_message,
        user_id
    )
#
async def call_apropriate_function_t(
    to_upload_file_g,
    sent_message_to_update_tg_p,
    is_unzip,
    is_unrar,
    is_untar
):
    #
    to_upload_file = to_upload_file_g
    if is_unzip:
        check_ifi_file = await unzip_me(to_upload_file_g)
        if check_ifi_file is not None:
            to_upload_file = check_ifi_file
    #
    if is_unrar:
        check_ife_file = await unrar_me(to_upload_file_g)
        if check_ife_file is not None:
            to_upload_file = check_ife_file
    #
    if is_untar:
        check_ify_file = await untar_me(to_upload_file_g)
        if check_ify_file is not None:
            to_upload_file = check_ify_file
    #
    response = {}
    LOGGER.info(response)
    user_id = sent_message_to_update_tg_p.reply_to_message.from_user.id
    final_response = await upload_to_gdrive(
        to_upload_file,
        sent_message_to_update_tg_p
    )
    LOGGER.info(final_response)
    #if to_upload_file:
        #if CUSTOM_FILE_NAME:
            #os.rename(to_upload_file, f"{CUSTOM_FILE_NAME}{to_upload_file}")
            #to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
        #else:
            #to_upload_file = to_upload_file

    #if cstom_file_name:
        #os.rename(to_upload_file, cstom_file_name)
        #to_upload_file = cstom_file_name
    #else:
        #to_upload_file = to_upload_file
    '''
    
    LOGGER.info(final_response)
    message_to_send = ""
    for key_f_res_se in final_response:
        local_file_name = key_f_res_se
        message_id = final_response[key_f_res_se]
        channel_id = str(AUTH_CHANNEL)[4:]
        private_link = f"https://t.me/c/{channel_id}/{message_id}"
        message_to_send += "🌹 <a href='"
        message_to_send += private_link
        message_to_send += "'>"
        message_to_send += local_file_name
        message_to_send += "</a>"
        message_to_send += "\n"
    if message_to_send != "":
        mention_req_user = f"<a href='tg://user?id={user_id}'>Your Requested Files</a>\n\n"
        message_to_send = mention_req_user + message_to_send
        message_to_send = message_to_send + "\n\n" + "#uploads"
    else:
        message_to_send = "<i>FAILED</i> to upload files. 😞😞"
    await sent_message_to_update_tg_p.reply_to_message.reply_text(
        text=message_to_send,
        quote=True,
        disable_web_page_preview=True
    )
    return True, None
    '''


# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164
async def check_progress_for_dl(aria2, gid, event, previous_message):
    try:
        file = aria2.get_download(gid)
        complete = file.is_complete
        is_file = file.seeder
        if not complete:
            if not file.error_message:
                msg = ""
                # sometimes, this weird https://t.me/c/1220993104/392975
                # error creeps up
                # TODO: temporary workaround
                downloading_dir_name = "N/A"
                try:
                    # another derp -_-
                    # https://t.me/c/1220993104/423318
                    downloading_dir_name = str(file.name)
                except:
                    pass
                #
                msg = f"\n<b>Downloading File:</b> `{downloading_dir_name}`"
                msg += f"\n<b>Progress:</b> <i>{file.progress_string()}</i>"
                msg += f"\n<b>Speed:</b> <i>{file.download_speed_string()}</i>"
                msg += f"\n<b>Total Size:</b> <i>{file.total_length_string()}</i>"

                if file.seeder is None :
                   msg += f"\n<b>Connections:</b> <i>{file.connections}</i>"
                else :
                   msg += f"\n<b>Peers:</b> <i>{file.connections}</i> | <b>Seeds:</b> <i>{file.num_seeders}</i>"

                msg += f"\n<b>Status:</b> <i>{file.status}</i>"
                msg += f"\n<b>ETA:</b> <i>{file.eta_string()}</i>"
                msg += f"\n<b>GID:</b> <code>{gid}</code>"
                inline_keyboard = []
                ikeyboard = []
                ikeyboard.append(InlineKeyboardButton("😔 Cancel This Process 😔", callback_data=(f"cancelfile {gid}").encode("UTF-8")))
                inline_keyboard.append(ikeyboard)
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                #msg += reply_markup
                LOGGER.info(msg)
                if msg != previous_message:
                    await event.edit(msg, reply_markup=reply_markup)
                    previous_message = msg
            else:
                msg = file.error_message
                await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                await event.edit(f"`{msg}`")
                return False
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await check_progress_for_dl(aria2, gid, event, previous_message)
        else:
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await event.edit(f"File Downloaded Successfully: `{file.name}`")
            return True
    except Exception as e:
        LOGGER.info(str(e))
        if " not found" in str(e) or "'file'" in str(e):
            await event.edit("Download Canceled")
            return False
        elif " depth exceeded" in str(e):
            file.remove(force=True)
            await event.edit("Download Auto Canceled\nYour Torrent/Link is Dead.")
            return False
        else:
            LOGGER.info(str(e))
            await event.edit("<u>error</u> :\n`{}` \n\n#error".format(str(e)))
            return
# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164


async def check_metadata(aria2, gid):
    file = aria2.get_download(gid)
    LOGGER.info(file)
    if not file.followed_by_ids:
        # https://t.me/c/1213160642/496
        return None
    new_gid = file.followed_by_ids[0]
    LOGGER.info("Changing GID " + gid + " to " + new_gid)
    return new_gid
