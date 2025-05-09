from policyengine_us.model_api import *


class ca_la_infant_supplement(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH
    label = "Los Angeles County infant supplement"
    defined_for = "in_la"

    def formula(household, period, parameters):
        p = parameters(period).gov.local.ca.la.dss.infant_supplement
        person = household.members
        is_in_group_home = household.any(
            person("is_in_foster_care_group_home", period)
        )
        base_amount = where(
            is_in_group_home, p.amount.group_home, p.amount.base
        )
        children = add(household, period, ["is_child"])
        eligible_person = person(
            "ca_la_infant_supplement_eligible_person", period
        )
        eligible_person_present = household.any(eligible_person)
        return base_amount * children * eligible_person_present
