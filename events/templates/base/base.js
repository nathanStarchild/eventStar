<script>
    async function postData(url, data){
        const response = await fetch(url, {
            method: 'POST', 
            headers: {
            // 'Content-Type': 'application/json'
            'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: data // body data type must match "Content-Type" header
        });
        return response.json(); // parses JSON response into native JavaScript objects
    }

    async function postForm($form){
        console.log($form.serialize())
        console.log($form)
        return postData($form.attr('action'), $form.serialize());
    }


    $(document).ready(function(){
        var theWindow = $(window);
        var bgImage = $(".backgroundImage");
        var aspect = bgImage.width() / bgImage.height();
        console.log(aspect)
        Promise.all(Array.from(document.images).filter(img => !img.complete).map(img => new Promise(resolve => { img.onload = img.onerror = resolve; }))).then(() => {
            bgImage = $(".backgroundImage");
            aspect = bgImage.width() / bgImage.height();
            console.log(aspect)
            resizeBg();
        });

        function resizeBg() {
            if ( (theWindow.width() / theWindow.height()) < aspect ) {
                let scaledWidth = theWindow.height() * aspect;
                let offset = (scaledWidth - theWindow.width()) / 2
                console.log(`-${offset.toFixed(0)}`)
                bgImage
                    .removeClass('bgwidth')
                    .addClass('bgheight')
                    .css("left", `-${offset.toFixed(0)}px`)
                    .css({"top": ""});
            } else {
                let scaledHeight = theWindow.width() / aspect;
                let offset = (scaledHeight - theWindow.height()) / 2
                console.log(offset)
                bgImage
                    .removeClass('bgheight')
                    .addClass('bgwidth')
                    .css("top", `-${offset.toFixed(0)}px`)
                    .css({"left": ""});
            }

        }

        theWindow.resize(resizeBg).trigger("resize");

    });
</script>