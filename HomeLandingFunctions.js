var student_ID = ""

function Login() {
    var username = document.getElementById('Username')
    var password = document.getElementById('Password')

    console.log(username.value, password.value)
    
    var request = new XMLHttpRequest()
    var type = ""

    request.open('GET', 'http://127.0.0.1:5000/' + username.value, true)
    request.onload = function () {

        var data = JSON.parse(this.response)
        var found = 0 

        if (request.status >= 200 && request.status < 400) {
            // console.log(data)

            for (i in Object.keys(data)){

                if(username.value == Object.keys(data)[i]){
                    if(password.value == data[Object.keys(data)[i]]){
                        found = 1;
                        console.log('Log In Successful!\n')

                        if(parseInt(username.value) < 9000){
                            type = "Student";
                            window.student_ID = username.value;
                        } else if(parseInt(username.value) >= 9000 && parseInt(username.value) < 10000){
                            type = "Teacher";
                            teacher_ID = username.value
                        } else {
                            type = "Admin";
                            admin_ID = username.value
                        }

                        if(type == "Student"){
                            location.replace("Student.html");
                        }
                        if(type == "Teacher"){
                            location.replace("Teacher.html");
                        }
                        if(type == "Admin"){
                            location.replace("Admin.html");
                        }

                        console.log(type)

                        break;
                    }
                }
            }

            if(found == 0){
                console.log("Error");
            }

        } else {
            console.log('error')
        }
    }

    request.send()

}