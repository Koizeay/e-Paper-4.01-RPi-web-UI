function displayImage(filename) {
    fetch(`/display?filename=${filename}`)
        .then(response => {
            if (response.ok) {
                Swal.fire({
                    title: "Success",
                    text: "Image sent for display",
                    showConfirmButton: true,
                    confirmButtonText: "OK",
                    confirmButtonColor: "#0e6327",
                    icon: "success"
                });
            } else {
                alert("Server error (file may not exist)");
            }
        });
}

function deleteImage(filename) {
    Swal.fire({
        title: "Are you sure?",
        text: "You will not be able to recover this image!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch("/manage/delete", {
                method: "POST",
                body: new URLSearchParams({ filename: filename }),
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            }).then(response => {
                if (response.ok) {
                    Swal.fire("Deleted!", "Your image has been deleted.", "success")
                        .then(() => location.reload());
                } else {
                    Swal.fire("Error", "Could not delete the image.", "error");
                }
            });
        }
    });
}

function renameImage(filename) {
    Swal.fire({
        title: "Enter new filename",
        input: "text",
        inputLabel: "New name (without extension)",
        inputPlaceholder: "Enter new name",
        showCancelButton: true,
        confirmButtonColor: "#0e6327",
        preConfirm: (newname) => {
            if (!newname) {
                Swal.showValidationMessage("Filename cannot be empty!");
            }
            return newname;
        }
    }).then((result) => {
        if (result.isConfirmed) {
            let newFilename = result.value + ".bmp";
            fetch("/manage/rename", {
                method: "POST",
                body: new URLSearchParams({ filename: filename, newname: newFilename }),
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            }).then(response => {
                if (response.ok) {
                    Swal.fire("Renamed!", "Your image has been renamed.", "success")
                        .then(() => location.reload());
                } else {
                    Swal.fire("Error", "Could not rename the image.", "error");
                }
            });
        }
    });
}
