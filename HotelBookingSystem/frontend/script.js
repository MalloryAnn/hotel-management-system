document.addEventListener("DOMContentLoaded", function () {
    const roomList = document.getElementById("room-list");

    async function fetchBookings() {
        try {
            const response = await fetch("fetch_bookings.php");

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const bookings = await response.json();

            console.log("Bookings fetched:", bookings);

            populateTable(bookings);
        } catch (error) {
            console.error("Error fetching bookings:", error);
            alert("Failed to load booking data. Please try again later.");
        }
    }

    function populateTable(bookings) {
        roomList.innerHTML = ""; // Clear existing rows

        bookings.forEach((booking) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td><button class="btn btn-primary btn-sm">${booking.action || "Check In"}</button></td>
                <td>${booking.guest_name}</td>
                <td>${booking.phone_number}</td>
                <td>${booking.email}</td>
                <td>${booking.room_id}</td>
                <td>${booking.room_type}</td>
                <td>$${booking.price.toFixed(2)}</td>
                <td>${booking.room_condition}</td>
                <td>${booking.status}</td>
                <td>${booking.room_view || "N/A"}</td>
                <td>${booking.amenities || "N/A"}</td>
                <td>${booking.check_in_date}</td>
                <td>${booking.check_out_date}</td>
            `;

            roomList.appendChild(row);
        });
    }

    async function bookRoom(event) {
        event.preventDefault(); // Prevent default form submission

        const guestName = document.getElementById("guest_name").value;
        const phoneNumber = document.getElementById("phone_number").value;
        const email = document.getElementById("email").value;
        const roomId = document.getElementById("room_id").value;
        const startDate = document.getElementById("start_date").value;
        const endDate = document.getElementById("end_date").value;

        try {
            const response = await fetch("book_room.php", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    guest_name: guestName,
                    phone_number: phoneNumber,
                    email: email,
                    room_id: roomId,
                    check_in_date: startDate,
                    check_out_date: endDate,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }


            const result = await response.json();

            console.log("Booking result:", result);

            alert(result.message || "Booking successful!");

            fetchBookings();
        } catch (error) {
            console.error("Error booking room:", error);
            alert("Failed to book room. Please try again later.");
        }
    }

    const bookingForm = document.getElementById("booking-form");
    if (bookingForm) {
        bookingForm.addEventListener("submit", bookRoom);
    }

    fetchBookings();
});
