import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

chat = []
mmsg = []
mmsg.append('k')

#vars
with open('config.txt') as file:
    port = file.readline()
    mip = file.readline()
fip = input("enter friend's ip: ")
name = input("enter your name: ")
#vars

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((mip, port))
sock.listen(2)
con, add = sock.accept()

with open('view.txt') as file:
    view = file.read()

with open('text.txt', 'w') as file:
    file.write(view)
    file.write('\n')


class Handler(FileSystemEventHandler):
    event = FileModifiedEvent('text.txt')

    def on_modified(self, event):
        with open('text.txt') as file:
            lines = file.readlines()
            try:
                text = lines[11].strip()
                opt = lines[7].strip()
            except IndexError:
                text = ''
                opt = ''
        #sending messages
        if text != '' and text != mmsg[-1]:
            mmsg.append(text)
            fad = (fip,port)
            text = name + '\t =>' + text
            con.sendto(text.encode('utf-8'), fad)

        if opt == 'Options:quit':
            fad = (fip,port)
            con.sendto((name + '\t =>your friend has been disconnected').encode('utf-8'), fad)
            con.close()
            with open('text.txt', 'w') as file:
                file.write('')
            sock.close()

if __name__ == '__main__':
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=False)
    observer.start()

    #catching messages
    try:
        while True:
            data = con.recv(4096)
            if not data:
                raise KeyboardInterrupt
            data = data.decode('utf-8')
            chat.append(data)
            with open('text.txt', 'w') as file:
                file.write(view + '\n')
                for msg in chat:
                    file.write(msg + '\n')
    except KeyboardInterrupt:
        con.close()
        with open('text.txt', 'w') as file:
            file.write('')
        observer.stop()
observer.join()

con.close()
sock.close()
