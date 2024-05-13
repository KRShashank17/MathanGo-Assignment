import os
import re
import json

def read_text_as_string(filename):
  script_dir = os.path.dirname(__file__)
  file_path = os.path.join(script_dir, filename)

  try:
    with open(file_path, 'r') as file:
      text = file.read()
      return text.strip()
  except FileNotFoundError:
    print(f"Error: File '{filename}' not found in the same directory.")
    return ""

def replace_newline_backslash(text_unfiltered):
    question_without_newline = text_unfiltered.replace('\n', ' ')
    pattern = r"(?<!\\)\\"
    question_without_backslash = re.sub(pattern, "\\\\", question_without_newline)
    question_without_section = question_without_backslash.replace("\\section*",' ')
    filtered_text = question_without_section.replace('\\', '\\\\')
    return filtered_text

def split_by_question_id(text):
  pattern = r"Question ID: "
  start_positions = [m.start() for m in re.finditer(pattern, text)]

  questions = []
  if start_positions:
    last_pos = 0
    for start_pos in start_positions:
      question = text[last_pos:start_pos]
      if "Answer" in question:
        # Preprocessing - remove '\n', replace '\' by '\\'
        filtered_question = replace_newline_backslash(question)
        questions.append(filtered_question)
      last_pos = start_pos + len(pattern)

    last_question = text[last_pos:]
    last_filtered_question = replace_newline_backslash(last_question)
    questions.append(last_filtered_question)
  else:
    questions = [text]

  return questions


def generate_question(q, question_id_match):
    int_tostring = str(question_id_match)
    indexofid = q.find(int_tostring) + 7
    endindex = q.find("(A) ")
    return q[indexofid: endindex].strip()

def generate_options(q):
    options_array = []
    indexofA = q.find("(A)")
    endofA = q.find("  (B)")
    option_A = q[indexofA + 4: endofA]
    options_array.append(option_A)
    # print(option_A)
    #
    indexofB = q.find("(B)")
    endofB = q.find("  (C)")
    option_B = q[indexofB + 4: endofB]
    options_array.append(option_B)
    # print(option_B)
    #
    indexofC = q.find("(C)")
    endofC = q.find("  (D)")
    option_C = q[indexofC + 4: endofC]
    options_array.append(option_C)
    # print(option_C)

    indexofD = q.find("(D)")
    endofD = q.find("Answer (")
    option_D = q[indexofD + 4: endofD]
    options_array.append(option_D)
    # print(option_D)

    # print(options_array)
    option_json_result = []
    for option_num, option in enumerate(options_array):
        option_json = {
            "optionNumber": option_num + 1,
            "optionText": option,
            "isCorrect": False
        }
        option_json_result.append(option_json)

    answer_index = q.find("Answer (")
    correct_option = q[answer_index + 8]
    # print(correct_option)

    indexof_crtoption = ord(correct_option) - ord('A')
    # print(indexof_crtoption)
    option_json_result[indexof_crtoption]["isCorrect"] = True
    # print(option_json_result)
    return option_json_result

def generate_solution(q):
    indexofsol = q.find("Sol")
    indexof_lastdollar = q.rfind("$")
    solution_match = ""
    if indexofsol != -1 and indexof_lastdollar > indexofsol:
        solution_match = q[indexofsol + len("Sol"):indexof_lastdollar + 1]
    # print(solution_match)
    return solution_match

def generate_json(allquestions):
    json_result = []
    for i,q in enumerate(all_questions):
        # print(f"{i+1} ------------------------------------------------------")
        # print(q)
        question_number = i+1

        pattern = r"\d{6}"                                      # Matches exactly 6 digits
        question_id_match = int (re.findall(pattern, q)[0])     # ['666666'] into 666666
        # print(question_id_match)

        question_match = generate_question(q,question_id_match)
        # print(question_match)

        option_json_result = generate_options(q)

        solution_match = generate_solution(q)

        curr_json = {
            "questionNumber" : question_number,
            "questionId" : question_id_match,
            "questionText" : question_match,
            "options": option_json_result,
            "solutionText": solution_match
        }
        # print(curr_json)
        json_result.append(curr_json)
    return json_result

def arrayof_json_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

text = read_text_as_string("Task.txt")
all_questions = split_by_question_id(text)
final_json_result = generate_json(all_questions)
# print(len(final_json_result))
# print(final_json_result)
arrayof_json_to_file(final_json_result, "result.json")
print("Result generated at result.json file")



