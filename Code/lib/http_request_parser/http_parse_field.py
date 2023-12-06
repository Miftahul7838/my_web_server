

class HttpParseField:

    def __init__(self, field_line, method) -> int:
        self.__field_line = field_line
        self.__method = method
        self.__fields = dict()

    def __has_content_length(self) -> int:
        field_list = self.__fields.keys()
        for field in field_list:
            field = field.lower()
            if field == 'content-length':
                return 200
        return 411

    def __rm_extra_sp(self, a_string:str) -> str:
        """takes out extra consecutive space

        Args:
        a_string: the string the needs to be parsed

        Returns
        new_string: string without any consecurity spaces
        """
        already_has_sp = False
        new_string = ""

        for char in a_string:
            if char == " " and not already_has_sp:
                new_string += char
                already_has_sp = True
            elif char != " ":
                new_string += char
                already_has_sp = False
        
        return new_string
        
    def __parse_field_line(self, field_info) -> int:
        """Checks to see if the requsted http fields is valid format

        Args:
        field_line: the http request fields

        Returns:
        is_valid_fields: a turple that contain either True or False and a 
                either none or the a dictionary containg all the 
                fields and their value depending on if the format
                is valid or not.
        """
        field_line = self.__field_line.split('\n')
        for field in field_line:
            if ':' in field:    
                field = field.strip().split(':')
                field_name = field[0]
                field_value = field[1]
                if " " in field_name:
                    return 400
                else:
                    self.__fields[field_name.lower()] = self.__rm_extra_sp(field_value)
            elif field == " " and field_line.index(field) == (len(field_line) - 1):
                return 400
        return 200
    
    def is_valid_field_line(self) -> tuple:
        field_info = None
        if len(self.__field_line) != 0:
            field_info = self.__parse_field_line(self.__field_line)
            if field_info == 200:
                if self.__method.lower() == 'post' or self.__method.lower()  == 'put':
                    has_cont_len = self.__has_content_length()
                    if has_cont_len == 200:
                        return (has_cont_len, self.__fields)
                    return (has_cont_len, None)
                elif self.__method.lower() != 'post' or self.__method.lower() != 'put':
                    return (200, self.__fields)
            return (400, None)



    