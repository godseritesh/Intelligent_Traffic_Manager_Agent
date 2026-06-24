import unittest
from reinforce_scheduler import ReinforceScheduler

class TestReinforceScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = ReinforceScheduler()

    def test_initial_state(self):
        self.assertEqual(self.scheduler.state, 'initial')

    def test_schedule_action(self):
        action = self.scheduler.schedule_action()
        self.assertIn(action, ['action1', 'action2', 'action3'])

    def test_reinforce(self):
        initial_reward = self.scheduler.reward
        self.scheduler.reinforce(10)
        self.assertEqual(self.scheduler.reward, initial_reward + 10)

    def test_reset(self):
        self.scheduler.reinforce(10)
        self.scheduler.reset()
        self.assertEqual(self.scheduler.reward, 0)

if __name__ == '__main__':
    unittest.main()