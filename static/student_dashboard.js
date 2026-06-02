// ---------------- TIMETABLE ----------------
fetch('/api/timetable')
.then(res => res.json())
.then(data => {

    let table = {"1":{}, "2":{}, "3":{}};

    let times = ["09:00","11:00","14:00"];
    let days = ["Monday","Tuesday","Wednesday","Thursday","Friday"];

    let body = document.getElementById("table-body");
    body.innerHTML = "";

    data.forEach(d => {
        let period = String(d.period);
        table[period][d.day] = d.sub;
    });

    Object.keys(table).forEach((p,i) => {
        let tr = document.createElement("tr");

        let row = `<td class="time">${times[i]}</td>`;

        days.forEach(day => {
            row += `<td>${table[p][day] || "-"}</td>`;
        });

        tr.innerHTML = row;
        body.appendChild(tr);
    });
});


// ---------------- STUDENT DATA ----------------
fetch('/api/student')
.then(res => res.json())
.then(data => {

    document.getElementById("student-img").src = "/static/" + data.image;
    document.getElementById("welcome").innerText = "Welcome back, " + data.name;

    // dropdown data
    document.getElementById("p-name").innerText = data.name;
    document.getElementById("p-reg").innerText = data.reg;
    document.getElementById("p-course").innerText = data.course;
    document.getElementById("p-year").innerText = data.year;
});


// ---------------- ATTENDANCE ----------------
fetch('/api/total')
.then(res => res.json())
.then(data => {

    let box = document.getElementById("attendance-box");
    box.innerHTML = "";

    data.forEach(sub => {

        let percent = (sub.present / sub.total) * 100;

        box.innerHTML += `
            <p>
                ${sub.subject.toUpperCase()} 
                ${sub.present}/${sub.total} - ${percent.toFixed(1)}%
            </p>
        `;
    });
});


// ---------------- PROFILE CLICK ----------------


function toggleProfile() {
    let menu = document.getElementById("profile-menu");
    menu.style.display = (menu.style.display === "block") ? "none" : "block";
}

fetch('/api/staff')
.then(res => res.json())
.then(data => {

    let box = document.getElementById("staff-box");
    box.innerHTML = "";

    data.forEach(d => {
        box.innerHTML += `
            <p><b>${d.sub.toUpperCase()}</b> - ${d.staff}</p>
        `;
    });
});


// ----------------staff data----------------

fetch('/api/staff')
.then(res => res.json())
.then(data => {
    let box = document.getElementById("staff-box");
    box.innerHTML = "";

    let shown = new Set();  // 🔥 track duplicates

    data.forEach(d => {

        if (!shown.has(d.subject)) {
            shown.add(d.subject);

            box.innerHTML += `
                <p>${d.subject} - ${d.staff}</p>
            `;
        }

    });
});


// ---------------- LOGOUT ----------------
function logout() {
    window.location.href = "/logout";
}

