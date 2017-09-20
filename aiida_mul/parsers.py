# -*- coding: utf-8 -*-

from aiida.parsers.parser import Parser
from aiida.parsers.exceptions import OutputParsingError
from aiida.orm.data.parameter import ParameterData

import json

class MultiplyParser(Parser):
    """Parser class for aiida_mul.
    """

    def parse_with_retrieved(self, retrieved):
        """Parse output data folder, store results in database.

        :param retrieved: 
        :returns: 
          bool: success
          node_list: list of new nodes to be stored in the db
        """
        success = False
        node_list = ()

        # Check that the retrieved folder is there
        try:
            out_folder = retrieved[self._calc._get_linkname_retrieved()]
        except KeyError:
            self.logger.error("No retrieved folder found")
            return success, node_list

        # check what is inside the folder
        list_of_files = out_folder.get_folder_list()

        # we need at least the output file name
        if self._calc._OUTPUT_FILE_NAME not in list_of_files:
            self.logger.error("Output file not found")
            return success, node_list

        try:
            with open( out_folder.get_abs_path(self._calc._OUTPUT_FILE_NAME) ) as f:
                out_dict = json.load(f)
        except ValueError:
            self.logger.error("Error parsing the output json")
            return success, node_list

        output_data = ParameterData(dict=out_dict)
        link_name = self.get_linkname_outparams()
        node_list = [(link_name, output_data)]
        success = True

        return success, node_list

