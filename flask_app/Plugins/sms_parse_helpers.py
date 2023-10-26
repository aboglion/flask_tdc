def replace_hebrew_with_english(text):
    hebrew_to_english = {
        'א': 'a',
        'ב': 'b',
        'ג': 'g',
        'ד': 'd',
        'ה': 'h',
        'ו': 'v',
        'ז': 'z',
        'ח': 'h',
        'ט': 't',
        'י': 'y',
        'כ': 'k',
        'ל': 'l',
        'מ': 'm',
        'נ': 'n',
        'ס': 's',
        'ע': 'a',
        'פ': 'p',
        'צ': 'tz',
        'ק': 'q',
        'ר': 'r',
        'ש': 'sh',
        'ת': 't',
        'ן': 'N',
        'ף': 'P',
        'ם': 'm',
    }
    illegal_chars = [' ', '-', '_', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '{', '}', ';', ':', ',', '<', '>', '?', '/', '|', '"', "'", '`', '~'] 
    translated_text = ''
    for char in text:
        if char in illegal_chars:
            translated_text +=str(illegal_chars.index(char))
            continue
        if char in hebrew_to_english:
            translated_text += hebrew_to_english[char]
        else:
            translated_text += char
    
    return translated_text

def had_a_style():
    h="""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
        <style>
        /* =========================================---------- */
        /* Style for the container holding the buttons */
    #butns {
        text-align: center;
        margin: 10px;
        position: sticky;
        top: 0;
        background-color: #BFC9CA;
        z-index: 100; 
    }

    /* Style for both buttons */
    .btn {
        background-color: #007bff; /* Blue color for the button background */
        color: #fff; /* White text color */
        border: none; /* Remove button border */
        padding: 10px 20px; /* Add padding to the button */
        margin-right: 10px; /* Add some spacing between buttons */
        cursor: pointer; /* Change cursor to pointer on hover */
        border-radius: 5px; /* Rounded corners */
    }

    /* Hover effect for both buttons */
    .btn:hover {
        background-color: #BFC9CA; /* Darker blue on hover */
    }

    /* Style for button text */
    .btn span {
        display: inline-block;
        transition: transform 0.2s ease-in-out;
    }

    /* Hover effect for button text */
    .btn:hover span {
        transform: scale(1.05); /* Enlarge text on hover */
    }

    /*=====================================----------- */



            table {
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }

            th, td {
                border: 1px solid #007bff;
                text-align: left;
                padding: 8px;
                background-color:#D5D8DC
            }


        .hidden-element {
                display: none;
            }

            /* אלמנט גלוי */
            .visible-element {
    display: table-row;

                    }
            .tag{
            text-align: center;
            font-weight: 900;
            color:#007bff;"
            }
            .tag :hover{
                color: brown;
            cursor: pointer;

            }
        </style>
    </head>
    <body>


    """

    return h

def btns():
    h=f'''<div id=butns >
                <button class="btn"  style="background-color: green" onclick="SHOW_ֹALL()">פתח לחיפוש כל טקסט </button>
                <button class="btn" style="background-color: orange"; onclick="HIDE()">הסתר הכל </button>
                <button class="btn" onclick="searchElementPrompt()">חפש לפי מספר הודעה</button>
                <a class="btn" style="background-color: pink;" href="/GROUPS.html">קבוצות</a>
            </div>'''
    return h

def js_end():
    h="""
    <script>
    function toggleClass(clname) {

    var elements = document.querySelectorAll("." + clname);
    

    elements.forEach(function(element) {
        element.classList.toggle('hidden-element');
        element.classList.toggle('visible-element');
    });
    }



    function SHOW_ֹALL(I=0) {

    // מצא את הטבלה לפי ה-ID שהועבר
    var table = document.getElementById('cat_tab'); 

    // חפש את כל השורות בטבלה
    var rows = table.getElementsByTagName('tr');

    // לעבור דרך כל השורות ולבדוק האם יש בהן את הטקסט והערך הבוליאני
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        row.classList.remove('hidden-element');
        row.classList.remove('visible-element');
        row.classList.add('visible-element');
        }
        if (I==0) alert("לחץ על CTRLּ+F")
    
    }

    function HIDE() {

    location.reload();
    
    }



    function searchElementPrompt() {
        SHOW_ֹALL(1)
        var searchInput = prompt('הזן מזהה'); // יצירת תיבת טקסט להזנת המזהה

        if (searchInput) {
            var elementToSearch = document.getElementById(searchInput); // מצא את האלמנט על פי המזהה שהמשתמש הזין

            if (elementToSearch) {
                // אם האלמנט נמצא, גלול אליו
                elementToSearch.scrollIntoView({ behavior: 'smooth', block: 'center' });
                elementToSearch.style.backgroundColor = "blue";
                elementToSearch.style.color = "yellow";
            } else {
                alert('מספר הודעה לא נמצא');
                HIDE() ;
            }
        }
    }

    </script>

    </body>
    </html>

    """
    return h

def gr_syle():
    h='''<style>
                    body {
                text-align: center;
                 
            }
            table {
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                margin: 0 auto; /* הכנסת הטבלה באמצע הדף */
                width: 50%;
                direction: rtl;
            }
            th, td {
                 direction: rtl;
                border: 1px solid #007bff;
                text-align: center;
                padding: 8px;
                background-color: #D5D8DC;
                color: rgb(85, 0, 255);
                
            }
            th {
                color: chartreuse;
                background-color: blue;
            }
                    </style>'''
    return h