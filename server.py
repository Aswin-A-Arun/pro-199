import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []

questions = [
    "What is the italian word for PIE? \n a. Mozarella \n b. pasty \n c. patty \n d. pizza",
    "water boils at 212 degrees in which scale? \n a. Fahrenheit \n b. Celsius \n c. rankine \n d.kelvin"
    "which creature has 3 hearts? \n a. octopus \n b. elephant \n c. walrus \n d. seal"
    "who was the character famous for being associated with sheep? \n a. tom \n b.mary \n c. johnny \n d. jack"
]
answers = ['d','a','b','a']

def clientthread(conn):
    score = 0
    conn.send("Welcome to the quiz".encode('utf-8'))
    conn.send("Choose an answer from the options given with the question".encode('utf-8'))
    conn.send("the quiz qill start now\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    while True:
        try: 
            message = conn.recieve(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send("Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrrect answer. try again later\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    NewThread = Thread(target = clientthread,args = (conn))