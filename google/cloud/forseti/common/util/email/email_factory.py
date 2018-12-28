# Copyright 2017 The Forseti Security Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Email factory to select connector"""

from google.cloud.forseti.common.util import logger
from google.cloud.forseti.common.util.email import sendgrid_connector

LOGGER = logger.get_logger(__name__)

EMAIL_CONNECTOR_FACTORY = {
    'sendgrid': sendgrid_connector.SendgridConnector
}


class InvalidInputError(Exception):
    """Exception raised when an invalid input is encountered."""

    def __init__(self, invalid_input):
        """Constructor for the base notifier.

        Args:
            invalid_input (dict): the invalid data format in question.
        """
        super(InvalidInputError, self).__init__(
            'Invalid input found: %s' % invalid_input)


class EmailFactory(object):
    """Email Factory to select connector."""

    def __init__(self, notifier_config):
        """Constructor for the email factory.

        Args:
            notifier_config (dict): Notifier configurations.
        """
        self.notifier_config = notifier_config
        if notifier_config.get('email_connector'):
            self.email_connector_config = (
                notifier_config.get('email_connector'))

    def get_connector(self):
        """Gets the connector and executes it.

        Returns:
            object: Connector class

        Raises:
            InvalidInputError: if not valid
        """
        if not self.notifier_config:
            raise InvalidInputError(self.notifier_config)
        if self.notifier_config.get('email_connector'):
            try:
                connector_name = self.email_connector_config.get('name')
                auth = self.email_connector_config.get('auth')
                sender = self.email_connector_config.get('sender')
                recipient = self.email_connector_config.get('recipient')
                return EMAIL_CONNECTOR_FACTORY[connector_name](sender,
                                                               recipient,
                                                               auth)
            except:
                LOGGER.exception(
                    'Error occurred while fetching connector details')
                raise InvalidInputError(self.notifier_config)
        # else block below is added for backward compatibility.
        else:
            try:
                connector_name = 'sendgrid'
                auth = self.notifier_config
                sender = self.notifier_config.get('sender')
                recipient = self.notifier_config.get('recipient')
                return EMAIL_CONNECTOR_FACTORY[connector_name](sender,
                                                               recipient,
                                                               auth)
            except:
                LOGGER.exception(
                    'Error occurred while fetching connector details')
                raise InvalidInputError(self.notifier_config)