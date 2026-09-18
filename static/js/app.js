// =====================================================
// GET COOKIE
// =====================================================
function getCookie(name) {

    const cookies =
        document.cookie.split(";");

    for (let cookie of cookies) {

        cookie = cookie.trim();

        if (cookie.startsWith(name + "=")) {

            return decodeURIComponent(
                cookie.substring(name.length + 1)
            );
        }
    }

    return null;
}

// =====================================================
// API HELPER
// =====================================================

async function apiRequest(url, options = {}) {

    const headers = {
        ...(options.headers || {})
    };

    const method =
        options.method?.toUpperCase();


    if (
        method &&
        ["POST", "PUT", "PATCH", "DELETE"].includes(method)
    ) {

        const csrfToken =
            getCookie("csrftoken");

        if (csrfToken) {

            headers["X-CSRFToken"] =
                csrfToken;

        }
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


// =====================================================
// AUTHENTICATION / NAVBAR
// =====================================================

async function checkAuthentication() {

    const authLinks =
        document.getElementById("authLinks");

    const userLinks =
        document.getElementById("userLinks");

    const dashboardLink =
        document.getElementById("dashboardLink");

    if (!authLinks || !userLinks) {
        return;
    }

    try {

        const user =
            await apiRequest(
                "/api/accounts/profile/"
            );

        // User is logged in

        authLinks.style.display = "none";
        userLinks.style.display = "inline-flex";

        if (dashboardLink) {

            if (user.role === "candidate") {

                dashboardLink.href =
                    "/candidate-dashboard/";

            } else if (user.role === "employer") {

                dashboardLink.href =
                    "/employer-dashboard/";
            }
        }

    } catch (error) {

        // User is not logged in

        authLinks.style.display = "inline-flex";
        userLinks.style.display = "none";
    }
}


// =====================================================
// LOGOUT
// =====================================================

async function logoutUser() {

    try {

        await apiRequest(
            "/api/accounts/logout/",
            {
                method: "POST"
            }
        );

        window.location.href = "/";

    } catch (error) {

        alert(error.message);
    }
}


// =====================================================
// LOAD CURRENT USER PROFILE
// =====================================================

async function loadCandidateProfile() {

    const usernameElement =
        document.getElementById(
            "candidateUsername"
        );

    const emailElement =
        document.getElementById(
            "candidateEmail"
        );

    if (!usernameElement || !emailElement) {
        return;
    }

    try {

        const user =
            await apiRequest(
                "/api/accounts/profile/"
            );

        usernameElement.textContent =
            user.username || "";

        emailElement.textContent =
            user.email || "";

    } catch (error) {

        usernameElement.textContent =
            "Not available";

        emailElement.textContent =
            "Not available";
    }
}


// =====================================================
// JOB SEARCH - HOME PAGE
// =====================================================

async function loadJobs() {

    const container =
        document.getElementById(
            "jobsContainer"
        );

    if (!container) {
        return;
    }

    const search =
        document.getElementById(
            "searchInput"
        )?.value || "";

    const location =
        document.getElementById(
            "locationInput"
        )?.value || "";

    const jobType =
        document.getElementById(
            "jobTypeInput"
        )?.value || "";

    const experience =
        document.getElementById(
            "experienceInput"
        )?.value || "";


    const params =
        new URLSearchParams();


    if (search) {
        params.append(
            "search",
            search
        );
    }

    if (location) {
        params.append(
            "location",
            location
        );
    }

    if (jobType) {
        params.append(
            "job_type",
            jobType
        );
    }

    if (experience) {
        params.append(
            "experience",
            experience
        );
    }


    try {

        const jobs =
            await apiRequest(
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

                    <a
                        href="/jobs/${job.id}/"
                        class="btn btn-primary"
                    >
                        View Job
                    </a>

                </div>

            `;
        });

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;
    }
}


// =====================================================
// CANDIDATE - BROWSE JOBS
// =====================================================

async function loadCandidateJobs() {

    const container =
        document.getElementById(
            "candidate-jobs"
        );

    if (!container) {
        return;
    }

    try {

        const jobs =
            await apiRequest(
                "/api/jobs/"
            );


        if (jobs.length === 0) {

            container.innerHTML =
                "<p>No jobs available.</p>";

            return;
        }


        container.innerHTML =
            jobs.map(job => `

                <div class="job-card">

                    <h3>
                        ${job.title}
                    </h3>

                    <p>
                        <strong>
                            Company:
                        </strong>
                        ${job.company_name}
                    </p>

                    <p>
                        <strong>
                            Location:
                        </strong>
                        ${job.location}
                    </p>

                    <p>
                        <strong>
                            Job Type:
                        </strong>
                        ${job.job_type}
                    </p>

                    <p>
                        <strong>
                            Experience:
                        </strong>
                        ${job.experience}
                    </p>

                    <p>
                        <strong>
                            Skills:
                        </strong>
                        ${job.skills}
                    </p>

                    <a
                        href="/jobs/${job.id}/"
                        class="btn btn-primary"
                    >
                        View Job & Apply
                    </a>

                </div>

            `).join("");

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;
    }
}


// =====================================================
// CANDIDATE - RESUME UPLOAD
// =====================================================

async function handleResumeUpload(event) {

    event.preventDefault();

    const file =
        document.getElementById(
            "resumeFile"
        )?.files[0];

    const message =
        document.getElementById(
            "resumeMessage"
        );


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


// =====================================================
// CANDIDATE - MY APPLICATIONS
// =====================================================

async function loadCandidateApplications() {

    const container =
        document.getElementById("applicationsContainer");

    if (!container) {
        return;
    }

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

            const isWithdrawn =
                application.status === "withdrawn";

            container.innerHTML += `

                <div class="application">

                    <h3>
                        ${application.job_title}
                    </h3>

                    <p>
                        <strong>Company:</strong>
                        ${application.company_name}
                    </p>

                    <p>
                        <strong>Status:</strong>

                        <span class="status">
                            ${application.status}
                        </span>
                    </p>

                    <p>
                        <strong>Applied:</strong>
                        ${
                            new Date(
                                application.applied_at
                            ).toLocaleDateString()
                        }
                    </p>

                    ${
                        application.cover_letter
                        ? `
                            <p>
                                <strong>Cover Letter:</strong>
                            </p>

                            <p>
                                ${application.cover_letter}
                            </p>
                        `
                        : ""
                    }

                    ${
                        isWithdrawn
                        ? `
                            <p>
                                <strong>
                                    This application has been withdrawn.
                                </strong>
                            </p>

                            <button
                                type="button"
                                onclick="
                                    reapplyForJob(
                                        ${application.job}
                                    )
                                "
                            >
                                Apply Again
                            </button>
                        `
                        : `
                            <div class="application-actions">

                                <button
                                    type="button"
                                    onclick="
                                        editApplication(
                                            ${application.id}
                                        )
                                    "
                                >
                                    Edit Application
                                </button>

                                <button
                                    type="button"
                                    onclick="
                                        withdrawApplication(
                                            ${application.id}
                                        )
                                    "
                                >
                                    Withdraw Application
                                </button>

                            </div>
                        `
                    }

                </div>

            `;
        });

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;
    }
}

// =====================================================
// CANDIDATE - UPDATE APPLICATION
// =====================================================

async function editApplication(applicationId) {

    const newCoverLetter =
        prompt(
            "Enter your new cover letter:"
        );

    if (newCoverLetter === null) {
        return;
    }

    try {

        await apiRequest(
            `/api/applications/${applicationId}/update/`,
            {
                method: "PATCH",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    cover_letter: newCoverLetter
                })
            }
        );

        alert(
            "Application updated successfully."
        );

        loadCandidateApplications();

    } catch (error) {

        alert(error.message);
    }
}

// =====================================================
// EMPLOYER - CREATE JOB
// =====================================================

async function handleJobCreation(event) {

    event.preventDefault();

    const message =
        document.getElementById(
            "jobMessage"
        );


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

        document
            .getElementById("jobForm")
            .reset();


    } catch (error) {

        message.textContent =
            error.message;
    }
}


// =====================================================
// EMPLOYER - APPLICATIONS
// =====================================================

async function loadEmployerApplications() {

    const container =
        document.getElementById(
            "employerApplications"
        );

    if (!container) {
        return;
    }

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

        applications.forEach(
            application => {

                container.innerHTML += `

                    <div class="application">

                        <h3>
                            ${application.job_title}
                        </h3>

                        <p>
                            Candidate:
                            <strong>
                                ${application.candidate}
                            </strong>
                        </p>

                        ${
                            application.resume_url
                            ? `
                                <p>
                                    Resume:

                                    <a
                                        href="${application.resume_url}"
                                        target="_blank"
                                        class="btn btn-outline"
                                    >
                                        View Resume
                                    </a>
                                </p>
                            `
                            : `
                                <p>
                                    Resume: Not available
                                </p>
                            `
                        }

                        <p>
                            <strong>
                                Cover Letter:
                            </strong>
                        </p>

                        <p>
                            ${
                                application.cover_letter ||
                                "No cover letter provided."
                            }
                        </p>

                        <p>
                            Current Status:

                            <span class="status">
                                ${application.status}
                            </span>
                        </p>

                        <label>
                            Update Status:
                        </label>

                        <select
                            onchange="
                                updateApplicationStatus(
                                    ${application.id},
                                    this.value
                                )
                            "
                        >

                            <option
                                value="applied"
                                ${
                                    application.status === "applied"
                                    ? "selected"
                                    : ""
                                }
                            >
                                Applied
                            </option>

                            <option
                                value="shortlisted"
                                ${
                                    application.status === "shortlisted"
                                    ? "selected"
                                    : ""
                                }
                            >
                                Shortlisted
                            </option>

                            <option
                                value="rejected"
                                ${
                                    application.status === "rejected"
                                    ? "selected"
                                    : ""
                                }
                            >
                                Rejected
                            </option>

                            <option
                                value="selected"
                                ${
                                    application.status === "selected"
                                    ? "selected"
                                    : ""
                                }
                            >
                                Selected
                            </option>

                        </select>

                    </div>

                `;
            }
        );

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;
    }
}


// =====================================================
// EMPLOYER - UPDATE APPLICATION STATUS
// =====================================================

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

                body:
                    JSON.stringify({
                        status: newStatus
                    })
            }
        );


        alert(
            "Application status updated."
        );


        // Reload applications
        loadEmployerApplications();

    } catch (error) {

        alert(error.message);
    }
}



// =====================================================
// EMPLOYER - NOTIFICATIONS
// =====================================================

async function loadEmployerNotifications() {

    const container =
        document.getElementById(
            "notificationsContainer"
        );

    if (!container) {
        return;
    }


    try {

        const notifications =
            await apiRequest(
                "/api/applications/notifications/"
            );


        container.innerHTML = "";


        if (notifications.length === 0) {

            container.innerHTML =
                "<p>No notifications.</p>";

            return;
        }


        notifications.forEach(
            notification => {

                container.innerHTML += `

                    <div class="notification">

                        <p>
                            ${notification.message}
                        </p>

                        <small>
                            ${new Date(
                                notification.created_at
                            ).toLocaleString()}
                        </small>

                    </div>

                `;
            }
        );

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;
    }
}


// =====================================================
// JOB DETAILS
// =====================================================

async function loadJobDetails() {

    const container =
        document.getElementById("jobDetails");

    if (!container) {
        return;
    }

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

        let user = null;

        try {
            user =
                await apiRequest(
                    "/api/accounts/profile/"
                );
        } catch (error) {
            // User is not logged in
        }

        let applyButton = "";

        if (user && user.role === "candidate") {

            applyButton = `
                <div id="applySection">

                    <button
                        onclick="applyForJob(${job.id})"
                        class="btn btn-primary"
                    >
                        Apply Now
                    </button>

                </div>
            `;

        } else if (!user) {

            applyButton = `
                <div id="applySection">

                    <p>
                        Please login as a candidate to apply.
                    </p>

                    <a
                        href="/login/"
                        class="btn btn-primary"
                    >
                        Login to Apply
                    </a>

                </div>
            `;

        }

        container.innerHTML = `

            <div class="card job-detail-card">

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

                ${applyButton}

            </div>

        `;

    } catch (error) {

        container.innerHTML =
            `<p>${error.message}</p>`;
    }
}


// =====================================================
// APPLY FOR JOB
// =====================================================

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

                body:
                    JSON.stringify({
                        job: jobId
                    })
            }
        );


        alert(
            "Application submitted successfully!"
        );


        window.location.href =
            "/candidate-dashboard/";

    } catch (error) {

        alert(error.message);
    }
}

// =====================================================
// LOGIN
// =====================================================

function setupLoginForm() {

    const loginForm =
        document.getElementById("loginForm");

    if (!loginForm) {
        return;
    }

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

                const data =
                    await apiRequest(
                        "/api/accounts/login/",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                username: username,
                                password: password
                            })
                        }
                    );


                message.textContent =
                    "Login successful!";


                if (data.role === "candidate") {

                    window.location.href =
                        "/candidate-dashboard/";

                } else if (data.role === "employer") {

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

// =====================================================
// REGISTER
// =====================================================

function setupRegisterForm() {

    const registerForm =
        document.getElementById("registerForm");

    if (!registerForm) {
        return;
    }

    registerForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const username =
                document.getElementById(
                    "regUsername"
                ).value;

            const email =
                document.getElementById(
                    "regEmail"
                ).value;

            const password =
                document.getElementById(
                    "regPassword"
                ).value;

            const role =
                document.getElementById(
                    "regRole"
                ).value;

            const companyName =
                document.getElementById(
                    "companyName"
                ).value;

            const message =
                document.getElementById(
                    "registerMessage"
                );


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

                            username: username,

                            email: email,

                            password: password,

                            role: role,

                            company_name:
                                companyName

                        })
                    }
                );


                message.textContent =
                    "Registration successful! Redirecting...";


                setTimeout(
                    () => {

                        window.location.href =
                            "/login/";

                    },
                    1000
                );


            } catch (error) {

                message.textContent =
                    error.message;
            }

        }
    );
}

async function withdrawApplication(applicationId) {

    const confirmWithdraw =
        confirm(
            "Are you sure you want to withdraw this application?"
        );

    if (!confirmWithdraw) {
        return;
    }

    try {

        await apiRequest(
            `/api/applications/${applicationId}/delete/`,
            {
                method: "DELETE"
            }
        );

        alert(
            "Application withdrawn successfully."
        );

        loadCandidateApplications();

    } catch (error) {

        alert(error.message);
    }
}

async function reapplyForJob(jobId) {

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
            "Application submitted again successfully."
        );

        loadCandidateApplications();

    } catch (error) {

        alert(error.message);
    }
}

// =====================================================
// PAGE INITIALIZATION
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        // Navbar
        checkAuthentication();

        // Login / Register
        setupLoginForm();
        setupRegisterForm();


        // Logout
        const logoutBtn =
            document.getElementById(
                "logoutBtn"
            );

        if (logoutBtn) {

            logoutBtn.addEventListener(
                "click",
                logoutUser
            );
        }


        // Candidate profile
        loadCandidateProfile();


        // Candidate jobs
        loadCandidateJobs();


        // Candidate applications
        loadCandidateApplications();
        


        // Employer applications
        loadEmployerApplications();


        // Employer notifications
        loadEmployerNotifications();


        // Resume form
        const resumeForm =
            document.getElementById(
                "resumeForm"
            );

        if (resumeForm) {

            resumeForm.addEventListener(
                "submit",
                handleResumeUpload
            );
        }


        // Job form
        const jobForm =
            document.getElementById(
                "jobForm"
            );

        if (jobForm) {

            jobForm.addEventListener(
                "submit",
                handleJobCreation
            );
        }


        // Job details
        loadJobDetails();
    }
);