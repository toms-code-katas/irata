from behave import step, use_step_matcher

use_step_matcher("re")


@step('I create a (default|customized) map')
def step_impl(context, map_type):
    """
    :type context: behave.runner.Context
    """
    print(map_type)
    raise NotImplementedError(u'STEP: Given I create a customized map')