import getpass, poplib, time

def read_auto_tester(mail_line, user):
    title_line = -8
    score_line = -6
    index = 0
    for line in mail_line:
        if 'student,init,compile,' in line:
            title_line = index
        if (user+',') in line:
            score_line = index
        index += 1
    split_line_title = mail_line[title_line].split(',')
    split_line_score = mail_line[score_line].split(',')

    for i in range(len(split_line_title)):
        print(split_line_title[i] + " : " + split_line_score[i])
        
def get_auto_tester(user, pass_):
    Mailbox = poplib.POP3_SSL('pop3.cdf.toronto.edu', '995') 
    Mailbox.user(user) 
    Mailbox.pass_(pass_) 
    numMessages = len(Mailbox.list()[1])
    auto_tester = []
    for i in range(numMessages):
        cur_msg = []
        is_auto_tester = False
        for msg in Mailbox.retr(i+1)[1]:
            msg_dc = msg.decode('utf-8')
            cur_msg.append(msg_dc)
            if 'Auto-Tester!' in msg_dc:
                is_auto_tester = True
        if is_auto_tester:
            auto_tester.append(cur_msg)
    return auto_tester

user = input('cdf user name: ')
pass_ = getpass.getpass("cdf password:")
auto_tester = get_auto_tester(user, pass_)
looping = True
auto_len = len(auto_tester)
while looping:
    print(" You have total of {} Auto_Tester email\n\
 Please Enter a number to see your result\n\
 Enter 'reload' to reload from cdf email\n\
 Enter 'areload' to Auto-reload until it finds \n\
    new Auto-test result Email\n\
 Enter 'exit' to exit the program".format(auto_len))
    user_input = input('Your selection: ')
    if user_input.isdigit() and 0 <= (int(user_input) - 1) < auto_len:
        read_auto_tester(auto_tester[int(user_input) - 1], user)
    if user_input.lower() == 'exit':
        looping = False
    if user_input.lower() == 'reload':
        print('Reloading')
        auto_tester = get_auto_tester(user, pass_)
        auto_len = len(auto_tester)
    if user_input.lower() == 'areload':
        print('Auto Reloading')
        auto_len_temp = len(auto_tester)
        i = 0
        while i < 20 and auto_len_temp == auto_len:
            print('No.{} Auto Reload attempt'.format(i + 1))
            time.sleep(60)
            auto_tester = get_auto_tester(user, pass_)
            auto_len_temp = len(auto_tester)
            i += 1
        auto_len = auto_len_temp
