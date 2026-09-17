async function apiRequest(url, options = {}) {

    const csrfToken =
        document.querySelector(
            'meta[name="csrf-token"]'
        )?.content;


    const headers = {
        ...(options.headers || {})
    };


    if (
        options.method &&
        ["POST", "PUT", "PATCH", "DELETE"]
            .includes(options.method.toUpperCase())
    ) {

        headers["X-CSRFToken"] =
            csrfToken;
    }


    const response = await fetch(url, {

        credentials: "same-origin",

        ...options,

        headers
    });


    let data = {};

    try {

        data = await response.json();

    } catch (error) {

        data = {};
    }


    if (!response.ok) {

        throw new Error(
            data.error ||
            data.detail ||
            "Something went wrong"
        );
    }


    return data;
}

async function loadJobs() {

    const container =
        document.getElementById("jobsContainer");

    if (!container) return;

    const search =
        document.getElementById("searchInput").value;

    const location =
        document.getElementById("locationInput").value;

    const jobType =
        document.getElementById("jobTypeInput").value;

    const experience =
        document.getElementById("experienceInput").value;


    const params = new URLSearchParams();

    if (search) {
        params.append("search", search);
    }

    if (location) {
        params.append("location", location);
    }

    if (jobType) {
        params.append("job_type", jobType);
    }

    if (experience) {
        params.append("experience", experience);
    }


    try {

        const jobs = await apiRequest(
            `/api/jobs/?${params.toString()}`
        );

        container.innerHTML = "";

        if (jobs.length === 0) {

            container.innerHTML =
                "<p>No jobs found.</p>";

            return;
        }


        jobs.forEach(job => {

            container.innerHTML += `

                <div class="job-card">

                    <h3>
                        ${job.title}
                    </h3>

                    <p>
                        <strong>
                            ${job.company_name}
                        </strong>
                    </p>

                    <p>
                        📍 ${job.location}
                    </p>

                    <p>
                        💼 ${job.job_type}
                    </p>

                    <p>
                        🎓 ${job.experience}
                    </p>

                    <p>
                        💰 ${job.salary || "Not specified"}
                    </p>

                    <p>
                        ${job.skills}
                    </p>

                    <a href="/jobs/${job.id}/">
                        <button>
                            View Job
                        </button>
                    </a>

                </div>

            `;
        });

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;
    }
}

const loginForm =
    document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const username =
                document.getElementById("username").value;

            const password =
                document.getElementById("password").value;

            const message =
                document.getElementById("loginMessage");


            try {

                const data = await apiRequest(
                    "/api/accounts/login/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            username,
                            password
                        })
                    }
                );


                message.textContent =
                    "Login successful!";


                if (data.role === "candidate") {

                    window.location.href =
                        "/candidate-dashboard/";

                } else {

                    window.location.href =
                        "/employer-dashboard/";
                }


            } catch (error) {

                message.textContent =
                    error.message;
            }
        }
    );
}

const registerForm =
    document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const username =
                document.getElementById("regUsername").value;

            const email =
                document.getElementById("regEmail").value;

            const password =
                document.getElementById("regPassword").value;

            const role =
                document.getElementById("regRole").value;

            const companyName =
                document.getElementById("companyName").value;


            const message =
                document.getElementById("registerMessage");


            try {

                await apiRequest(
                    "/api/accounts/register/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            username,
                            email,
                            password,
                            role,
                            company_name: companyName

                        })
                    }
                );


                message.textContent =
                    "Registration successful! Redirecting...";


                setTimeout(() => {

                    window.location.href =
                        "/login/";

                }, 1000);


            } catch (error) {

                message.textContent =
                    error.message;
            }
        }
    );
}

const resumeForm =
    document.getElementById("resumeForm");

if (resumeForm) {

    resumeForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const file =
                document.getElementById("resumeFile").files[0];

            const message =
                document.getElementById("resumeMessage");


            if (!file) {

                message.textContent =
                    "Please select a resume.";

                return;
            }


            const formData =
                new FormData();

            formData.append(
                "resume_file",
                file
            );


            try {

                await apiRequest(
                    "/api/applications/resume/",
                    {
                        method: "POST",
                        body: formData
                    }
                );


                message.textContent =
                    "Resume uploaded successfully.";

            } catch (error) {

                message.textContent =
                    error.message;
            }
        }
    );
}

async function loadCandidateApplications() {

    const container =
        document.getElementById(
            "applicationsContainer"
        );

    if (!container) return;


    try {

        const applications =
            await apiRequest(
                "/api/applications/my/"
            );


        container.innerHTML = "";


        if (applications.length === 0) {

            container.innerHTML =
                "<p>You haven't applied for any jobs yet.</p>";

            return;
        }


        applications.forEach(application => {

            container.innerHTML += `

                <div class="application">

                    <h3>
                        ${application.job_title}
                    </h3>

                    <p>
                        ${application.company_name}
                    </p>

                    <p>
                        Status:
                        <span class="status">
                            ${application.status}
                        </span>
                    </p>

                    <p>
                        Applied:
                        ${new Date(
                            application.applied_at
                        ).toLocaleDateString()}
                    </p>

                </div>

            `;
        });


    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;
    }
}

document.addEventListener(
    "DOMContentLoaded",
    loadCandidateApplications
);

const jobForm =
    document.getElementById("jobForm");

if (jobForm) {

    jobForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const message =
                document.getElementById("jobMessage");


            const jobData = {

                title:
                    document.getElementById(
                        "jobTitle"
                    ).value,

                description:
                    document.getElementById(
                        "jobDescription"
                    ).value,

                company_name:
                    document.getElementById(
                        "companyName"
                    ).value,

                location:
                    document.getElementById(
                        "jobLocation"
                    ).value,

                salary:
                    document.getElementById(
                        "jobSalary"
                    ).value,

                job_type:
                    document.getElementById(
                        "jobType"
                    ).value,

                experience:
                    document.getElementById(
                        "jobExperience"
                    ).value,

                skills:
                    document.getElementById(
                        "jobSkills"
                    ).value
            };


            try {

                await apiRequest(
                    "/api/jobs/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(jobData)
                    }
                );


                message.textContent =
                    "Job posted successfully.";

                jobForm.reset();


            } catch (error) {

                message.textContent =
                    error.message;
            }
        }
    );
}

async function loadEmployerApplications() {

    const container =
        document.getElementById(
            "employerApplications"
        );

    if (!container) return;


    try {

        const applications =
            await apiRequest(
                "/api/applications/employer/"
            );


        container.innerHTML = "";


        if (applications.length === 0) {

            container.innerHTML =
                "<p>No applications yet.</p>";

            return;
        }


        applications.forEach(application => {

            container.innerHTML += `

                <div class="application">

                    <h3>
                        ${application.job_title}
                    </h3>

                    <p>
                        Candidate:
                        ${application.candidate}
                    </p>

                    <p>
                        Status:
                        ${application.status}
                    </p>


                    <select
                        onchange="updateApplicationStatus(
                            ${application.id},
                            this.value
                        )"
                    >

                        <option value="applied"
                            ${application.status === "applied" ? "selected" : ""}>
                            Applied
                        </option>

                        <option value="shortlisted"
                            ${application.status === "shortlisted" ? "selected" : ""}>
                            Shortlisted
                        </option>

                        <option value="rejected"
                            ${application.status === "rejected" ? "selected" : ""}>
                            Rejected
                        </option>

                        <option value="selected"
                            ${application.status === "selected" ? "selected" : ""}>
                            Selected
                        </option>

                    </select>

                </div>

            `;
        });


    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;
    }
}

async function updateApplicationStatus(
    applicationId,
    newStatus
) {

    try {

        await apiRequest(
            `/api/applications/${applicationId}/status/`,
            {
                method: "PATCH",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    status: newStatus
                })
            }
        );

        alert(
            "Application status updated."
        );


    } catch (error) {

        alert(error.message);
    }
}

document.addEventListener(
    "DOMContentLoaded",
    loadEmployerApplications
);

async function loadJobDetails() {

    const container =
        document.getElementById("jobDetails");

    if (!container) return;


    const pathParts =
        window.location.pathname
            .split("/")
            .filter(Boolean);

    const jobId =
        pathParts[pathParts.length - 1];


    try {

        const job =
            await apiRequest(
                `/api/jobs/${jobId}/`
            );


        container.innerHTML = `

            <div class="card">

                <h1>
                    ${job.title}
                </h1>

                <h3>
                    ${job.company_name}
                </h3>

                <p>
                    📍 ${job.location}
                </p>

                <p>
                    💼 ${job.job_type}
                </p>

                <p>
                    🎓 ${job.experience}
                </p>

                <p>
                    💰 ${job.salary || "Not specified"}
                </p>

                <h3>
                    Description
                </h3>

                <p>
                    ${job.description}
                </p>

                <h3>
                    Skills
                </h3>

                <p>
                    ${job.skills}
                </p>

                <button
                    onclick="applyForJob(${job.id})"
                >
                    Apply Now
                </button>

            </div>

        `;

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;
    }
}

async function applyForJob(jobId) {

    try {

        await apiRequest(
            "/api/applications/apply/",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    job: jobId
                })
            }
        );


        alert(
            "Application submitted successfully!"
        );


    } catch (error) {

        alert(error.message);
    }
}