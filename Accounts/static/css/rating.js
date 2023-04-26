var stars = document.querySelectorAll('.star')
                        document.addEventListener("click", function (e) {
                        var index = e.target.dataset.value;

                        for (var i = 0; i < 5; ++i){
                            stars[i].classList.remove('active')
                        }
                        for (var i = 0; i < index; ++i){
                            stars[i].classList.add('active')
                        }
                        });