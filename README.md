1. Data Fetching Issue

    Description:
        The timetable data stored in the database is not being displayed on the student dashboard or admin dashboard timetable.

    Symptoms:
        Dashboard loads successfully
        No timetable data appears despite existing records

    Possible Causes:
        Incorrect or missing queryset (timetable_qs) in the backend
        Improper filtering logic
        Template not rendering the correct context variables

2. Department & Semester Filtering Not Working

    Description:
        Selecting a department or semester does not update the timetable dynamically.

    Symptoms:
        Dropdown selection has no effect
        Same (or empty) timetable is displayed

    Possible Causes:
        Form data not being submitted correctly (GET/POST issue)
        Selected values not passed to backend
        Incorrect filtering logic in view

3. PDF Download Feature Not Working

    Description:
        The "Download PDF" button is present but not functional.

    Possible Causes:
        Missing backend implementation
        JavaScript function not properly defined


⚠️ Timetable Generation Algorithm Issue:
    1. Weekly Class Limit Violation:
    
        The algorithm does not properly enforce the limit of maximum 3 classes per subject per week, resulting in over-allocation and an unbalanced timetable.

    2. Duplicate Subject in a Day

        A subject is sometimes scheduled more than once in a single day, which violates the rule of one class per subject per day and reduces timetable quality.

    3. Incomplete Data Fetching

        The system fails to retrieve full data from the database, leading to partial timetable generation with missing subjects and fewer classes.

📌 Summary
    ❌ Weekly constraints not enforced
    ❌ Duplicate subject allocation in a day
    ❌ Incomplete data retrieval

➡️ Result: The generated timetable is inconsistent, incomplete, and unreliable