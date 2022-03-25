UPDATE enrollment set transmissionstatusid = 3, transmissionstatusdate = getdate()
WHERE enrollmentid in (
       SELECT enrollmentid from enrollment e
       INNER JOIN offering o
              ON o.offeringid = e.offeringid
       INNER JOIN AcademicYearBlock ayb
              ON ayb.AcademicYearBlockId = o.AcademicYearBlockId
       INNER JOIN block b
              ON b.BlockId = ayb.blockid
       INNER JOIN student s
              ON s.personid = e.personid
       INNER JOIN course c
              ON c.Courseid = o.courseid
       INNER JOIN MUSemester m
              ON m.MUSemesterId = b.muSemesterid
       INNER JOIN AcademicYear ay
              ON ay.AcademicYearId = ayb.AcademicYearId
       INNER JOIN REF_MU_Enrollment_Courses rmc
              ON rmc.TERM = m.TextAbbreviated + CASE WHEN m.MUSemesterId = 3
                     THEN RIGHT(ay.text,4)
                     ELSE LEFT(ay.text,4)
                     END AND rmc.SESSION_CODE = b.myZou_Block
                     AND rmc.[CATALOG_NBR] = c.UniversityCourseCode
                     AND 'M' + Convert( varchar(4), CASE WHEN b.YearOfStudyId in (3, 4)
                           THEN (SELECT yearofstudyid
                                  FROM StudentYearOfStudy
                                  WHERE AcademicYearid = ay.AcademicYearId AND personid = e.PersonId AND IsDeleted = 0)
                           ELSE b.YearOfStudyId END) = rmc.CLASS_SECTION
       WHERE rmc.CLASS_NBR = {{CLASS_NBR from row}}
       AND s.[MUStudentNumber]  = {{EMPLID from row}}
       AND e.TransmissionStatusId = 2
)
