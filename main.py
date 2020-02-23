import twitter_Image_Video as TIV
import threading
import time
import queue


def tweets2image_process(q,q2,twitter):

    username = q.get()

    print("\ngrab "+username+" tweets is processing...")

    profile_url = twitter.download_pro_url(username)

    tweets = twitter.download_tweets(username)

    TIV.Tweets2image(username, profile_url, tweets)

    q2.put(username)

    print("\ndone")


def Image2Video_process(q1, q2):

    if not q2.empty():

        username =  q2.get()

        print("\n"+username+" image to video is processing...")

        TIV.imgToVideo(username) 

        print ("\n"+"done")


def username_input (q1, q2):

    if not q1.full():

        id = input("\n Twitter id ?")
        q1.put(id)

    else:
        print("\n wait a minute...")

    time.sleep(0.2)
    return username_input (q1, q2)


def main():
    q1 = queue.Queue(maxsize=4)

    q2 = queue.Queue()

    twitter = TIV.status("keys")

    t_input = threading.Thread(name="username_input",
                                target= username_input, 
                                 args=(q1, q2))

    t_input.start()

    while True:
      if not q1.empty():

        t_t2i = threading.Thread(name="tweets2image_process", 
                                  target=tweets2image_process, 
                                   args=(q1, q2,twitter))
        t_t2i.start()  
      if not q2.empty():
        t_i2v = threading.Thread(name="Image2Video_process", 
                                  target=Image2Video_process, 
                                    args=(q1, q2))
        t_i2v.start()
      time.sleep(0.1)  

if __name__ == '__main__':

    main()

