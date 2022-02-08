from typing import Union


def file_compares(old_file: list, new_file: list):
    if len(old_file) != len(new_file):
        return (None, "Error")
    
    diffs = []
    for old, new in zip(old_file, new_file):
        if old['subject'] != new['subject']:
            return (None, "Error")
        if len(old['tasks']) != len(new['tasks']):
            return (None, "Error")
        diffs_one_subject = []
        for old_task, new_task in zip(old['tasks'], new['tasks']):
            if old_task['max_grade'] != new_task['max_grade']:
                return (None, "Error")
            if old_task['alias'] != new_task['alias']:
                return (None, "Error")
            if old_task['current_grade'] != new_task['current_grade']:
                diffs_one_subject.append({
                    'task': new_task['alias'],
                    'ball': {
                        'abs_difference': round(abs(new_task['current_grade'] - old_task['current_grade']), 2),
                        'is_new_bigger': new_task['current_grade'] - old_task['current_grade'] > 0,
                        'current_ball': new_task['current_grade'],
                        'old_ball': old_task['current_grade'],
                        'max_grade': new_task['max_grade'],
                    }
                })
        if len(diffs_one_subject) != 0:
            diffs.append({'subject': new['subject'], 'tasks': diffs_one_subject})
    return (diffs, "OK")


def get_msg_from_diff(diffs: list) -> str:
    msg = ""
    for diff_subject in diffs:
        tmp_msg = ""
        for diff_task in diff_subject['tasks']:
            tmp_msg += '🟢' if diff_task['ball']['is_new_bigger'] else '🔴'
            tmp_msg += f" {diff_task['task']}:\n"
            tmp_msg += f"{diff_task['ball']['old_ball']} -> {diff_task['ball']['current_ball']} (из {diff_task['ball']['max_grade']})"
            tmp_msg += f" ({'%2B' if diff_task['ball']['is_new_bigger'] else '-'}{diff_task['ball']['abs_difference']})\n"
        msg += f"{diff_subject['subject']}\n{tmp_msg}\n"
    return msg