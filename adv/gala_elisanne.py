from core.advbase import *
from slot.d import *
from slot.a import *

def module():
    return Gala_Elisanne

class Gala_Elisanne(Adv):
    comment = 'no s2, s!cleo ss after s1'
    a3 = ('primed_att',0.10)

    conf = {}
    conf['slots.a'] = BB()+The_Chocolatiers()
    conf['slots.frostbite.a'] = conf['slots.a']
    conf['slots.d'] = Gaibhne_and_Creidhne()
    conf['acl'] = """
        `s1
        `s4,s=1
        `s3
        `fsf, x=4
    """
    conf['coabs'] = ['Bow','Tobias', 'Renee']
    conf['share'] = ['Summer_Luca', 'Summer_Cleo']
    
    def init(self):
        self.buff_class = Teambuff if self.condition('buff all team') else Selfbuff

    @staticmethod
    def prerun_skillshare(adv, dst):
        adv.buff_class = Dummy if adv.slots.c.ele != 'water' else Teambuff if adv.condition('buff all team') else Selfbuff

    def prerun(self):
        self.s2.autocharge_init(900).on()

    def s1_proc(self, e):
        self.buff_class(e.name,0.3,15).on()

    def s2_proc(self, e):
        self.energy.add(3)


if __name__ == '__main__':
    from core.simulate import test_with_argv
    test_with_argv(None, *sys.argv)