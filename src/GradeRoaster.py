class GradeRoaster:
    def __init__(self, ACAD_GROUP, TERM, STRM, SESSION_CODE, CLASS_NBR, CRSE_ID, SUBJECT, CATALOG_NBR, CLASS_SECTION,
                 DESCR, INSTRUCTOR_ID, GRADE, EMPLID, LAST_NAME, FIRST_NAME, GRD_RSTR_TYPE_SEQ, ACAD_CAREER):
        self.ACAD_GROUP = ACAD_GROUP
        self.TERM = TERM
        self.STRM = STRM
        self.SESSION_CODE = SESSION_CODE
        self.CLASS_NBR = CLASS_NBR
        self.CRSE_ID = CRSE_ID
        self.SUBJECT = SUBJECT
        self.CATALOG_NBR = CATALOG_NBR
        self.CLASS_SECTION = CLASS_SECTION
        self.DESCR = DESCR
        self.INSTRUCTOR_ID = INSTRUCTOR_ID
        self.GRADE = GRADE
        self.EMPLID = EMPLID
        self.LAST_NAME = LAST_NAME
        self.FIRST_NAME = FIRST_NAME
        self.GRD_RSTR_TYPE_SEQ = GRD_RSTR_TYPE_SEQ
        self.ACAD_CAREER = ACAD_CAREER

    def get_grade(self):
        return self.GRADE
