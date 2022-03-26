function myFunction() {
    let timerInterval
    Swal.fire({
        title: 'Estimating Age!',

        timer: 10000,
        backdrop: `rgba(0,0,123,0.4)`,
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading()
            timerInterval = setInterval(() => {
                const content = Swal.getHtmlContainer()
                if (content) {
                    const b = content.querySelector('b')
                    if (b) {
                        b.textContent = Swal.getTimerLeft()
                    }
                }
            }, 100)
        },
        willClose: () => {
            clearInterval(timerInterval)
        }
    }).then((result) => {
        /* Read more about handling dismissals below */
        if (result.dismiss === Swal.DismissReason.timer) {
            console.log('I was closed by the timer')
        }
    })
}

function imageView(image) {
    Swal.fire({
        imageUrl: image,
        imageHeight: "500PX",
        width: "1000px",
        imageAlt: 'A tall image',
        confirmButtonText: 'Close',
        confirmButtonColor: '#7962ca',
    })

}

function noiseimage(image) {
    Swal.fire({
        title: 'Sweet!',
        text: 'Modal with a custom image.',
        imageUrl: image,
        imageWidth: 400,
        imageHeight: 200,
        imageAlt: 'Custom image',
    })

}


