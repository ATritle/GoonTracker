function formatTimestamp(timestamp) {

    if (!timestamp) {
        return "Unknown";
    }

    let normalized =
        timestamp.replace(" ", "T");

    const date =
        new Date(normalized);

    if (isNaN(date)) {
        return timestamp;
    }

    const formattedDate =
        date.toLocaleString(
            "en-US",
            {
                month: "short",
                day: "numeric",
                hour: "numeric",
                minute: "2-digit"
            }
        );

    const now =
        new Date();

    const diffMs =
        now.getTime() -
        date.getTime();

    const diffMinutes =
        Math.floor(
            diffMs / 60000
        );

    let ago = "";

    if (diffMinutes <= 1) {

        ago = "just now";

    } else if (diffMinutes < 60) {

        ago = `${diffMinutes} min ago`;

    } else if (diffMinutes < 1440) {

        const hours =
            Math.floor(
                diffMinutes / 60
            );

        ago =
            hours === 1
            ? "1 hour ago"
            : `${hours} hours ago`;

    } else {

        const days =
            Math.floor(
                diffMinutes / 1440
            );

        ago =
            days === 1
            ? "1 day ago"
            : `${days} days ago`;
    }

    return `${formattedDate} (${ago})`;
}


async function loadData() {

    try {

        const response =
            await fetch(
                "/current_status"
            );

        const data =
            await response.json();

        const statusEl =
            document.getElementById(
                "status"
            );

        statusEl.innerText =
            data.status;

        if (
            data.status === "AGREEMENT"
        ) {

            statusEl.style.color =
                "#4CAF50";

        } else {

            statusEl.style.color =
                "#ff9800";
        }

        let html = "";

        for (
            const report
            of data.reports
        ) {

            const timestamp =
                report.report_time ||
                report.collected_at;

            html += `
                <div class="report">

                    <div class="source-row">

                        <span class="source">
                            ${report.source}
                        </span>

                        <span class="map">
                            ${report.map}
                        </span>

                    </div>

                    <div class="report-time">
                        ${formatTimestamp(timestamp)}
                    </div>

                </div>
            `;
        }

        document.getElementById(
            "reports"
        ).innerHTML =
            html;

    } catch (error) {

        document.getElementById(
            "status"
        ).innerText =
            "OFFLINE";

        document.getElementById(
            "status"
        ).style.color =
            "#f44336";

        console.error(error);
    }
}

loadData();

setInterval(
    loadData,
    60000
);