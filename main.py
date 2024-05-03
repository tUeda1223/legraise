# coding: utf-8
# For use in pythonista on iOS
import motion
from scene import *
import math
import time
import speech
import sound
from random import randint as rd
import console

# paramater
rollCondition = 40  # °
dt = 0.1
saveCount = 30
keepTime = [3.5, 1.0]

# effect
keepRemainEffect = 'digital:PowerUp2'
keepRemainEndEffect = 'arcade:Coin_5'
keepEndEffect = 'arcade:Explosion_7'
# voice
first = ["レッグレイズ", "さぁ，いくよ", "さぁ，うごこう"]
advice = ["割れた腹筋を目指すのにおすすめだよ", "足を浮かせたままやれば，お腹にかなり効くよ", "六つに割れたシックスパックを目指そう", "足は曲げず，伸ばしておこなおう", "腹筋を強化したい人におすすめの動きだよ"]
before = ["がんばれ", "good", "いいね", "いいよ", "行ける", "ok", "その感じ", "よし", "よしよし", "yes", "そういいね", "そうその感じ", "great"]
after = ["ばっっちり", "びっくり", "excellent", "fantastic", "いい感じ", "いい動き", "輝いてるよ", "完璧", "nice", "いいぞいいぞ", "キレッキレ", "お見事", "すごい", "やれる", "やるね"]
half = ["どんどんいこうか", "自分を追い込んで行こう", "よし，ペースアップだ", "あと半分", "ペーズ上げていこう"]
last = ["汗が輝いてるよ．ビューティフル", "いい汗かいたね", "いい動きだったよ", "いやーお疲れ様", "完璧だね", "体を動かすっていいね", "お疲れ様", "最高だったよ", "たくさん動いたね", "よくやりきったね", "よくやった", "なんとかやりきったね", "筋肉が喜んでるよ"]


class MyScene (Scene):
    def setup(self):
        console.set_idle_timer_disabled(True)

        global scale
        scale = self.size.w/10
        motion.start_updates()
        # pitch,roll,yawメータの半径
        self.R = scale
        self.raising = 0
        self.saveCount = saveCount
        self.keepRemain = -1
        self.keepTime = keepTime[0]
        self.keepStart = False
        self.keepEnd = False
        self.instCx = self.size.w * 0.5
        self.instCy = self.size.h * 0.5 - 3*self.R
        self.faceCx = self.size.w * 0.3
        self.faceCy = self.size.h * 0.5
        self.countCx = self.size.w * 0.5
        self.countCy = self.size.h * 0.5 + 3*self.R
        self.resetCx = self.size.w * 0.1
        self.resetCy = self.size.h * 0.9
        self.resetBotton = SpriteNode(
            'pzl:Button1', position=(self.resetCx, self.resetCy))
        # self.add_child(self.resetBotton)
        self.count = 0
        speech.say(first[rd(0, len(first)-1)])

    def touch_ended(self, touch):
        touchLocation = self.point_from_scene(touch.location)
        if touchLocation in self.resetBotton.frame:
            self.count = 0

    def stop(self):
        sound.stop_all_effects()
        console.set_idle_timer_disabled(False)

    def draw(self):
        # wait
        time.sleep(dt)
        # update roll
        gravity_vectors = motion.get_attitude()
        pitch, roll, yaw = [x for x in gravity_vectors]
        roll = roll*180/3.1415926
        roll_sin = math.sin(math.radians(roll))
        roll_cos = math.cos(math.radians(roll))
        # condition
        if roll > rollCondition:
            if self.keepStart == False:
                self.keepRemain = self.keepTime
            self.keepStart = True
            if self.keepRemain > 0:
                sound.play_effect(keepRemainEffect)
                self.keepRemain -= dt
            else:
                if self.keepEnd == False:
                    sound.play_effect(keepRemainEndEffect)
                    speech.say(before[rd(0, len(before)-1)])
                self.keepEnd = True
        else:
            self.keepStart = False
            self.keepRemain = -1
            if self.keepEnd == True:
                sound.play_effect(keepEndEffect)
                self.count += 1
                if self.count % self.saveCount == 5:
                    speech.say(advice[rd(0, len(advice)-1)])
                elif self.count % self.saveCount == self.saveCount - 20:
                    speech.say("あと20回")
                elif (self.count % self.saveCount) == (self.saveCount // 2):
                    speech.say(half[rd(0, len(half)-1)])
                    self.keepTime = keepTime[1]
                elif self.count % self.saveCount == self.saveCount - 10:
                    speech.say("あと10回")
                elif self.count % self.saveCount == self.saveCount - 5:
                    speech.say("あと5回")
                elif self.count % self.saveCount == self.saveCount - 3:
                    speech.say("あと3回")
                elif self.count % self.saveCount == self.saveCount - 1:
                    speech.say("ラスト1回")
                elif self.count % self.saveCount == 0:
                    speech.say(last[rd(0, len(last)-1)])
                    self.keepTime = keepTime[0]
                else:
                    speech.say(after[rd(0, len(after)-1)])
            self.keepEnd = False

        # redraw screen
        background(1, 1, 1)
        fill(1, 1, 1)
        # draw human
        stroke(self.keepStart, 0, 0)
        stroke_weight(2)
        ellipse(self.faceCx-self.R, self.faceCy-self.R, self.R*2, self.R*2)
        line(self.faceCx, self.faceCy-self.R,
             self.faceCx-self.R, self.faceCy-2*self.R)
        line(self.faceCx-self.R, self.faceCy-2*self.R,
             self.faceCx, self.faceCy-2*self.R,)
        line(self.faceCx, self.faceCy-self.R,
             self.faceCx+self.R, self.faceCy-2*self.R)
        line(self.faceCx+self.R, self.faceCy-2*self.R,
             self.faceCx+self.R+3*roll_cos*self.R, self.faceCy-2*self.R+3*roll_sin*self.R)
        # write role
        tint(0, 0, 0, 1)
        text(str(round(roll, 0))+"°", font_name='Helvetica', font_size=24.0,
             x=self.faceCx, y=self.faceCy+self.R+20, alignment=5)
        # write instruction
        if self.keepStart and self.keepEnd:
            strTmp = '下げて！！'
        elif self.keepStart and not self.keepEnd:
            strTmp = 'キープ！！'
        else:
            strTmp = '上げて！！'
        text(strTmp, font_name='Helvetica', font_size=int(
            self.size.w/5), x=self.instCx, y=self.instCy, alignment=5)
        # write count
        text("回数: "+str(self.count), font_name='Helvetica',
             font_size=self.size.w/5, x=self.countCx, y=self.countCy, alignment=5)
        # write count
        text("Reset", font_name='Helvetica', font_size=24.0,
             x=self.resetCx, y=self.resetCy, alignment=5)
        # write keepRemain
        if self.keepStart:
            text(str(round(self.keepRemain, 1)), font_name='Helvetica',
                 font_size=24.0, x=self.faceCx, y=self.faceCy, alignment=5)


if __name__ == "__main__":
    scene = run(MyScene(), PORTRAIT, show_fps=True)