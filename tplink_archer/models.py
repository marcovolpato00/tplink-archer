from typing import List, Optional
from enum import Enum, auto

from .exceptions import StackParseError, SectionNotFoundError


class WifiFreq(Enum):
    WIFI_2G = auto()
    WIFI_5G = auto()

########################################################################################################################


class Section(object):
    def __init__(self, identifier: str, values: dict):
        """Init Section object

        :param identifier: Section identifier
        :type identifier: str
        :param values: Section values dictionary
        :type values: dict
        """
        self.identifier = identifier
        self.values = values

    def __repr__(self):
        return f'<Section(identifier={self.identifier})>'

    def to_text(self) -> str:
        """Get Section in plain text format

        :rtype: str
        """

        values = ''
        for key in self.values.keys():
            value = self.values.get(key)
            values = values + f'{key}={value}\n'

        return f'{self.identifier}\n' + values

########################################################################################################################


class Stack(object):
    def __init__(self, data: str):
        """Init Stack object

        :param data: Stack data in plain text
        :type data: str
        """
        self.sections: Optional[List[Section]] = None
        self.parse(data)

    def parse(self, data: str):
        """Parse plain text into Stack

        :param data:
        """

        if data is None:
            return ValueError
        sections = self.__get_sections(data)
        parsed_sections = self.__parse_sections(sections)
        self.sections = parsed_sections

    def get_section(self, identifier: str) -> Optional[Section]:
        """Get Section from identifier or None if not found

        :param identifier:
        :rtype: Optional[Section]
        """

        if not self.sections:
            return None
        for s in self.sections:
            if s.identifier == identifier:
                return s
        raise SectionNotFoundError

    @staticmethod
    def __get_sections(stack: str) -> List[str]:
        """Split plain text stack into plain text sections

        :param stack: plain text stack
        :rtype: List[str]
        """

        sections = []

        open_index = 0
        while open_index != -1:
            try:
                open_index = stack[1:].find('[')  # next section opening index
                new_stack = stack[open_index + 1:]  # stack without current section
                if open_index != -1:  # if not last section
                    s = stack[:open_index]  # isolate section
                    sections.append(s)
                    stack = new_stack
                else:
                    sections.append(new_stack)  # last section, all text remaining
            except Exception:
                raise StackParseError

        return sections

    @staticmethod
    def __parse_lines_to_section(sections: str) -> Section:
        """Parse plain text section into Section object

        :param sections: plain text section
        :rtype: Section
        """

        lines = sections.split('\n')

        identifier = lines[0]

        section_values = {}
        for pair in lines[1:]:
            pair_split = pair.split('=')
            section_values.update({pair_split[0]: pair_split[1]})

        return Section(identifier, section_values)

    def __parse_sections(self, sections) -> List[Section]:
        """Parse all sections into Sections list

        :param sections: list of plain text sections
        :rtype: List[Section]
        """

        for i, s in enumerate(sections):
            sections[i] = self.__parse_lines_to_section(s)
        return sections

    def to_dict(self) -> dict:
        """ returns stack in dict format """

        sections = []
        for s in self.sections:
            sections.append(
                {
                    'identifier': s.identifier,
                    'values': s.values
                }
            )
        return {
            'sections': sections
        }

    def to_text(self) -> str:
        """Returns Stack in text format
        """

        stack = ''
        for section in self.sections:
            stack = stack + section.to_text()
        return stack

    def __eq__(self, other):
        """Checks if the other object is equal

        :param other: other object to compare
        :rtype: bool
        """

        if len(self.sections) != len(other.sections):
            return False

        for i, section in enumerate(self.sections):
            other_section = other.sections[i]
            if section.values.keys() != other_section.values.keys() or section.identifier != other_section.identifier:
                return False

        return True

########################################################################################################################


class BaseSettingsElement(object):
    """Base object for settings elements
    """

    def __init__(self, identifier: str):
        """Init BaseSettingsElement

        :param identifier: element identifier
        """
        self.identifier = identifier

    def __repr__(self):
        return f'<BaseSettingsElement(identifier={self.identifier})>'

    @property
    def raw_identifier(self):
        return self.identifier[1:].split(']')[0]

    def to_section(self) -> Section:
        """Returns element to section format
        """

        return Section(
            identifier=self.identifier,
            values={}
        )

    def to_text(self) -> str:
        """Returns element to text format
        """

        section = self.to_section()
        return section.to_text()

########################################################################################################################


class DHCPLease(BaseSettingsElement):
    def __init__(self, identifier: str, ip_address: str, mac_address: str, is_enabled: bool):
        super().__init__(identifier)
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.is_enabled = is_enabled

    def __repr__(self):
        return (f'<DHCPLease(identifier={self.identifier},'
                f'ip_address={self.ip_address},'
                f'mac_address={self.mac_address},'
                f'is_enabled={str(self.is_enabled)})>')

    def to_section(self) -> Section:
        """Returns lease to Section object

        :rtype: Section
        """

        section_values = {
            'chaddr': self.mac_address,
            'yiaddr': self.ip_address,
            'enable': '1' if self.is_enabled else '0'
        }
        return Section(
            identifier=self.identifier,
            values=section_values
        )

########################################################################################################################


class PortForwardingRule(BaseSettingsElement):
    def __init__(self, identifier: str, client_ip_address: str, internal_port: str, external_port: str,
                 is_enabled: bool, protocol: str, internal_port_end: Optional[str] = None,
                 external_port_end: Optional[str] = None):
        super().__init__(identifier)
        self.client_ip_address = client_ip_address
        self.internal_port = internal_port
        self.external_port = external_port
        self.is_enabled = is_enabled
        self.protocol = protocol

        self.internal_port_end = internal_port_end
        self.external_port_end = external_port_end
        if not internal_port_end:
            self.internal_port_end = internal_port
        if not external_port_end:
            self.internal_port_end = external_port

    def __repr__(self):
        return (f'<PortForwardingRule(identifier={self.identifier},'
                f'client_ip_address={self.client_ip_address},'
                f'internal_port_range={self.internal_port_range},'
                f'external_port_range={self.external_port_range},'
                f'protocol={self.protocol},'
                f'is_enabled={str(self.is_enabled)})>')

    @property
    def internal_port_range(self):
        return f'{self.internal_port}-{self.internal_port_end}'

    @property
    def external_port_range(self):
        return f'{self.external_port}-{self.external_port_end}'

    def to_section(self) -> Section:
        """Returns rule to Section object

        :rtype: Section
        """

        section_values = {
            'externalPort': self.external_port,
            'internalPort': self.internal_port,
            'X_TP_ExternalPortEnd': self.external_port_end,
            'X_TP_InternalPortEnd': self.internal_port_end,
            'internalClient': self.client_ip_address,
            'portMappingProtocol': self.protocol,
            'portMappingEnabled': '1' if self.is_enabled else '0',
        }
        return Section(
            identifier=self.identifier,
            values=section_values
        )
