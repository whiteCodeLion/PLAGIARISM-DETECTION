        const form = document.querySelector('#upload-form');
        const resultDiv = document.querySelector('#result');

        form.addEventListener('submit', event => {
            event.preventDefault();
            const formData = new FormData(form);
            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    const plagiarismDetected = data.plagiarism_detected;
                    if (plagiarismDetected) {
                        resultDiv.innerHTML = 'Plagiarism detected! The similarity score is ' + data.similarity.toFixed(2);
                    } else {
                        resultDiv.innerHTML = 'No plagiarism detected!';
                    }
                })
                .catch(error => {
                    resultDiv.innerHTML = 'An error occurred: ' + error.message;
                });
        });
