
// ---------------- LOAD TEACHER ----------------
fetch('/api/teacher')
.then(res => res.json())
.then(data => {
    document.getElementById("welcome").innerText =
        "Welcome " + data.teacherName;
});

// ---------------- LOAD SUBJECTS ----------------
fetch('/api/teacher/timetable')
.then(res => res.json())
.then(data => {

    let div = document.getElementById("subjects");
    let select = document.getElementById("classSelect");

    let shown = new Set();
    div.innerHTML = "";
    select.innerHTML = "<option value=''>Select Class</option>";

    data.forEach(t => {

        let key = t.sub + t.year;

        if (!shown.has(key)) {
            shown.add(key);

            div.innerHTML += `
                <p onclick="loadToday('${t.sub}','${t.year}')">
                    ${t.sub} (${t.year})
                </p>
            `;
        }

        select.innerHTML += `
            <option value="${t.sub}|${t.year}">
                ${t.sub} (${t.year})
            </option>
        `;
    });
});

// ---------------- LOAD TODAY ----------------
function loadToday(sub, year) {

    fetch(`/api/today_attendance?sub=${sub}&year=${year}`)
    .then(res => res.json())
    .then(data => {

        let div = document.getElementById("attendance");

        div.innerHTML = `
            <h4>${sub}</h4>
            <p><b>Present:</b> ${data.present.join(", ")}</p>
            <p><b>Absent:</b> ${data.absent.join(", ")}</p>

            <input type="date" id="editDate">
            <button onclick="editAttendance('${sub}','${year}')">
                Update
            </button>
        `;
    });
}

// ---------------- EDIT ATTENDANCE ----------------
function editAttendance(sub, year) {

    let d = document.getElementById("editDate").value;

    if (!d) {
        alert("Select date");
        return;
    }

    let parts = d.split("-");
    let date = `${parts[2]}/${parts[1]}/${parts[0]}`;

    fetch(`/api/get_attendance?sub=${sub}&year=${year}&date=${date}`)
    .then(res => res.json())
    .then(data => {

        let div = document.getElementById("attendance");
        div.innerHTML = `<h4>Edit (${date})</h4>`;

        data.students.forEach(s => {

            let checked = data.present.includes(String(s.reg)) ? "checked" : "";

            div.innerHTML += `
                <p>
                    <input type="checkbox" value="${s.reg}" ${checked}>
                    ${s.name}
                </p>
            `;
        });

        div.innerHTML += `
            <button onclick="saveAttendance('${sub}','${year}','${date}')">
                Save
            </button>
        `;
    });
}

// ---------------- SAVE ----------------
function saveAttendance(sub, year, date) {

    let checked = document.querySelectorAll("#attendance input:checked");

    let present = [];

    checked.forEach(c => present.push(c.value));

    fetch('/api/save_attendance', {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({sub, year, date, present})
    })
    .then(res => res.json())
    .then(msg => alert(msg.msg));
}

// ---------------- SEARCH ----------------
function search() {

    let q = document.getElementById("searchBox").value;

    fetch(`/api/teacher/search?q=${q}`)
    .then(res => res.json())
    .then(data => {

        let div = document.getElementById("result");
        div.innerHTML = "";

        // REG SEARCH
        if (data.type === "reg") {

            data.data.forEach(d => {
                div.innerHTML += `
                    <p>${d.subject} → ${d.present}/${d.total} (${d.percent}%)</p>
                `;
            });
        }

        // DATE SEARCH
        else if (data.type === "date") {

            div.innerHTML += `<p><b>${data.subject}</b></p>`;
            div.innerHTML += `<p>Present: ${data.present.join(", ")}</p>`;
            div.innerHTML += `<p>Absent: ${data.absent.join(", ")}</p>`;
        }

        // SUBJECT SEARCH
        else if (data.type === "subject") {

            data.data.forEach(d => {
                div.innerHTML += `
                    <p>${d.date} → ${d.present.join(", ")}</p>
                `;
            });
        }

        else {
            div.innerHTML = data.msg;
        }
    });
}

// ---------------- PROFILE ----------------
function showProfile() {
    document.getElementById("profileModal").style.display = "block";

    fetch('/api/teacher')
    .then(res => res.json())
    .then(d => {
        document.getElementById("profileData").innerHTML = `
            <p>${d.teacherName}</p>
            <p>${d.email}</p>
        `;
    });
}

function closeProfile() {
    document.getElementById("profileModal").style.display = "none";
}

// ---------------- PASSWORD CHANGE ----------------
function changePassword() {

    let p = document.getElementById("newPass").value;

    fetch('/api/change_password', {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({password:p})
    })
    .then(res=>res.json())
    .then(d=>alert(d.msg));
}

// ---------------- LOGOUT ----------------
function logout(){
    window.location = "/logout";
}

// ---------------- IMAGE UPLOAD ----------------
function uploadImage(){

    let file = document.getElementById("imageInput").files[0];
    let selected = document.getElementById("classSelect").value;
    let date = document.getElementById("uploadDate").value;

    if(!file || !selected || !date){
        alert("Fill all fields");
        return;
    }

    let [sub,year] = selected.split("|");

    let parts = date.split("-");
    let d = `${parts[2]}/${parts[1]}/${parts[0]}`;

    let form = new FormData();
    form.append("image",file);
    form.append("sub",sub);
    form.append("year",year);
    form.append("date",d);

    fetch('/api/mark_attendance',{method:"POST",body:form})
    .then(res=>res.json())
    .then(d=>alert(d.msg));
}
// ---------------- TIMETABLE ----------------
fetch('/api/teacher/timetable')
.then(res => res.json())
.then(data => {

    let days = ["Monday","Tuesday","Wednesday","Thursday","Friday"];
    let table = document.querySelector("#tt tbody");

    table.innerHTML = "";  // clear

    days.forEach(day => {

        let row = `<tr><td>${day}</td>`;

        for(let p = 1; p <= 3; p++) {

            let found = data.find(d =>
                d.day.toLowerCase() === day.toLowerCase() &&
                d.period == p
            );

            if(found){
                row += `<td>${found.sub}<br>Year ${found.year}</td>`;
            } else {
                row += `<td>-</td>`;
            }
        }

        row += "</tr>";
        table.innerHTML += row;
    });
});
