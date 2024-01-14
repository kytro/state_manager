#!/usr/bin/env python
# -*- coding: utf-8 -*
from collections import OrderedDict
from datetime import datetime
from logging import getLogger

from voluptuous import Optional, Required, Schema

from homeassistant.const import CONF_NAME, CONF_ICON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.config_validation import string, positive_int
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.template import Template
from homeassistant.util import slugify
from .helper import create_input_datetime, create_input_number, create_automation

CONF_FREQUENCY = 'frequency'
CONF_NOTIFY = 'notify'

_LOGGER = getLogger(__name__)


async def async_setup_platform(hass: HomeAssistant, config, async_add_entities, discovery_info=None):
    name = config[CONF_NAME]
    notify = config.get(CONF_NOTIFY)
    icon = config.get(CONF_ICON)

    letzte_ausfuehrung_name = name + " Letzte Ausführung"
    letzte_ausfuehrung_input_datetime_name = 'input_datetime.' + slugify(letzte_ausfuehrung_name)

    erinnern_um_name = name + " Erinnern um"
    erinnern_um_input_datetime_name = 'input_datetime.' + slugify(erinnern_um_name)

    frequenz_name = name + ' Frequenz'
    frequenz_input_number_name = 'input_number.' + slugify(frequenz_name)

    pause_name = name + ' Pause'
    pause_input_number_name = 'input_number.' + slugify(pause_name)

    await create_input_datetime(letzte_ausfuehrung_name, True, False, icon=icon)
    await create_input_datetime(erinnern_um_name, False, True, icon=icon)
    await create_input_number(frequenz_name, 1, 99999, 1, 'box', 'Tage', icon=icon)
    await create_input_number(pause_name, 1, 99999, 1, 'box', 'Tage', icon=icon)
    await create_automation_for_notification(name, letzte_ausfuehrung_input_datetime_name,
                                             erinnern_um_input_datetime_name,
                                             frequenz_input_number_name, pause_input_number_name, notify)
    await create_automation_for_notification_action(name)

    async_add_entities([StateManagerEntity(name, notify, letzte_ausfuehrung_input_datetime_name,
                                       erinnern_um_input_datetime_name, frequenz_input_number_name, pause_input_number_name)], False)


async def create_automation_for_notification(name: str, letzte_ausfuehrung_name: str,
                                             erinnern_um_name: str,
                                             frequenz_name: str,
                                             pause_name: str,
                                             notify_list: list):
    internal_name = slugify(name)

    notification_list = []

    for notify in notify_list:
        notification_list.append(
            {
                'service': 'notify.{}'.format(notify),
                'data': {
                    'title': name,
                    'message': Template(
                        "{% set tage = (((as_timestamp(now().date()) - state_attr('" + letzte_ausfuehrung_name + "', 'timestamp')) | int /60/60/24) | round(0)) - (states('" + frequenz_name + "') | int) %} " + name + " ausstehend seit {{ 'heute.' if tage == 0 else 'gestern.' if tage == 1 else tage | string + ' Tagen.' }}"),
                    'data': {
                        'importance': 'default',
                        'channel': 'Information',
                        'tag': internal_name + 'Notification',
                        'color': 'green',
                        'actions': [
                            {
                                'action': internal_name + 'Done',
                                'title': 'Erledigt'
                            }
                        ]
                    }
                }
            }
        )

    data = {
        'alias': name,
        'trigger': [
            {
                'platform': 'time',
                'at': [erinnern_um_name]
            }
        ],
        'condition': [
            {
                'condition': 'template',
                'value_template': Template(
                    "{{ (((as_timestamp(now().date()) - state_attr('" + letzte_ausfuehrung_name + "', 'timestamp')) | int /60/60/24) | round(0)) >= (states('" + frequenz_name + "') | int) and ((((as_timestamp(now().date()) - state_attr('" + letzte_ausfuehrung_name + "', 'timestamp')) | int /60/60/24) | round(0)) - (states('" + frequenz_name + "') | int)) % (states('" + pause_name + "') | int) == 0 }}")
            }
        ],
        'action': notification_list,
        'mode': 'single',
        'max_exceeded': 'WARNING',
        'max': 10,
        'trace': {
            'stored_traces': 5
        }
    }

    await create_automation(OrderedDict(data))


async def create_automation_for_notification_action(name: str):
    internal_name = slugify(name)

    data = {
        'alias': name + ' erledigt',
        'trigger': [
            {
                'platform': 'event',
                'event_type': ['mobile_app_notification_action'],
                'event_data': {
                    'action': internal_name + 'Done'
                }
            }
        ],
        'action': [
            {
                'service': 'state_manager.done',
                'entity_id': 'state_manager.{}'.format(internal_name)
            }
        ],
        'mode': 'single',
        'max_exceeded': 'WARNING',
        'max': 10,
        'trace': {
            'stored_traces': 5
        }
    }

    await create_automation(OrderedDict(data))


class StateManagerEntity(Entity):
    def __init__(self, name: str, notify: list, letzte_ausfuhrung_input_datetime: str, erinnern_um_input_datetime: str,
                 frequenz_input_number: str, pause_input_number: str):
        self._name = name
        self._notify = notify
        self._letzte_ausfuhrung_input_datetime = letzte_ausfuhrung_input_datetime
        self._erinnern_um_input_datetime = erinnern_um_input_datetime
        self._frequenz_input_number = frequenz_input_number
        self._pause_input_number = pause_input_number

    async def async_update(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def device_state_attributes(self):
        return {
            'last_execution': self._letzte_ausfuhrung_input_datetime,
            'remind_at': self._erinnern_um_input_datetime,
            'frequency': self._frequenz_input_number,
            'pause': self._pause_input_number
        }

    async def done(self):
        if self._notify:
            data = {
                'message': 'clear_notification',
                'data': {
                    'tag': slugify(self._name) + 'Notification'
                }
            }

            for notify in self._notify:
                await self.hass.services.async_call('notify', notify, data)

        data = {
            'entity_id': self._letzte_ausfuhrung_input_datetime,
            'date': datetime.now().strftime("%Y-%m-%d")
            # 'time': datetime.now().strftime("%H:%M")
        }

        await self.hass.services.async_call('input_datetime', 'set_datetime', data)