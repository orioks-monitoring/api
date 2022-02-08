from typing import Union

import aiohttp
import asyncio

import json
import config


async def _get_disciplines_info(session: aiohttp.ClientSession):
    async with session.get('https://orioks.miet.ru/api/v1/student/disciplines', headers=config.ORIOKS) as resp:
        return await resp.json()


async def _get_student_id(session: aiohttp.ClientSession) -> int:
    url = f'https://orioks.miet.ru/api/v1/student'
    async with session.get(url, headers=config.ORIOKS) as resp:
        student_info = await resp.json()
        return student_info['record_book_id']


async def _get_current_data(session: aiohttp.ClientSession, disciplines) -> list:
    async def _get_discipline_detailed_info(session: aiohttp.ClientSession, discipline_id: str):
        url = f'https://orioks.miet.ru/api/v1/student/disciplines/{discipline_id}/events'
        async with session.get(url, headers=config.ORIOKS) as resp:
            return await resp.json()
    
    """return: [{'subject': s, 'tasks': [t], 'ball': full_ball}, ...]"""  # full_ball без последней оценки, т.к. в API нет :( 
    json_to_save = []
    for discipline in disciplines:
        sum_ball = 0
        marks = await _get_discipline_detailed_info(session=session, discipline_id=discipline['id'])
        one_discipline = []
        for mark in marks:
            try:
                _alias = mark['alias']
            except KeyError:
                _alias = mark['type']
            try:
                _current_grade = mark['current_grade']
            except:
                _current_grade = 0

            one_discipline.append({'alias': _alias, 'current_grade': _current_grade, 'max_grade': mark['max_grade']})
            sum_ball += mark['current_grade'] if 'current_grade' in mark.keys() else 0
        json_to_save.append({
            'subject': discipline['name'],
            'tasks': one_discipline,
            'ball': round(sum_ball, 2),
        })
    return json_to_save


async def get_student_info():
    async with aiohttp.ClientSession() as session:
        student_id = await _get_student_id(session)
        _disciplines = await _get_disciplines_info(session=session)
        detailed_info = await _get_current_data(session=session, disciplines=_disciplines)
    return (student_id, detailed_info)