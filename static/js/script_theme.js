document.addEventListener('DOMContentLoaded', function () {
    // Theme button & modal
    const themeBtn = document.querySelector('#theme'); 
    const themeModal = document.querySelector('.customize-theme');

    // Font size selection
    const fontSizes = document.querySelectorAll('.choose-size span');
    const root = document.documentElement; 

    // Color selection
    const colorPalette = document.querySelectorAll('.choose-color span');

    // Background selection
    const Bg1 = document.querySelector('.bg-1');
    const Bg2 = document.querySelector('.bg-2');
    const Bg3 = document.querySelector('.bg-3');

    // ========== OPEN & CLOSE THEME MODAL ==========
    const openThemeModal = () => {
        themeModal.style.display = 'grid';
    };

    const closeThemeModal = (e) => {
        if (e.target.classList.contains('customize-theme')) {
            themeModal.style.display = 'none';
        }
    };

    
    // Add event listeners
    themeBtn.addEventListener('click', openThemeModal);
    themeModal.addEventListener('click', closeThemeModal);

    // ========== CHANGE FONT SIZE ==========
    fontSizes.forEach(size => {
        size.addEventListener('click', () => {
            document.querySelector('.choose-size .active')?.classList.remove('active');
            size.classList.add('active');

            let fontSize;
            if (size.classList.contains('font-size-1')) {
                fontSize = '10px';
                root.style.setProperty('--sticky-top-left', '5.4rem');
                root.style.setProperty('--sticky-top-right', '5.4rem');
            } else if (size.classList.contains('font-size-2')) {
                fontSize = '13px';
                root.style.setProperty('--sticky-top-left', '5.4rem');
                root.style.setProperty('--sticky-top-right', '-7rem');
            } else if (size.classList.contains('font-size-3')) {
                fontSize = '15px';
                root.style.setProperty('--sticky-top-left', '-2rem');
                root.style.setProperty('--sticky-top-right', '-17rem');
            } else if (size.classList.contains('font-size-4')) {
                fontSize = '17px';
                root.style.setProperty('--sticky-top-left', '-5rem');
                root.style.setProperty('--sticky-top-right', '-25rem');
            } else if (size.classList.contains('font-size-5')) {
                fontSize = '18px';
                root.style.setProperty('--sticky-top-left', '-10rem');
                root.style.setProperty('--sticky-top-right', '-33rem');
            }

            document.querySelector('html').style.fontSize = fontSize;
        });
    });

    // ========== CHANGE PRIMARY COLOR ==========
    colorPalette.forEach(color => {
        color.addEventListener('click', () => {
            document.querySelector('.choose-color .active')?.classList.remove('active');
            color.classList.add('active');

            let primaryColor;
            if (color.classList.contains('color-1')) {
                primaryColor = "hsl(255,75%,60%)";
            } else if (color.classList.contains('color-2')) {
                primaryColor = "hsl(52,75%,60%)";
            } else if (color.classList.contains('color-3')) {
                primaryColor = "hsl(352,75%,60%)";
            } else if (color.classList.contains('color-4')) {
                primaryColor = "hsl(152,75%,60%)";
            } else if (color.classList.contains('color-5')) {
                primaryColor = "hsl(202,75%,60%)";
            }

            root.style.setProperty('--color-primary', primaryColor);
        });
    });

    // ========== CHANGE BACKGROUND THEME ==========
    let lightColorLightness;
    let darkColorLightness;
    let whiteColorLightness;

    const changeBg = () => {
        root.style.setProperty('--light-color-lightness', lightColorLightness);
        root.style.setProperty('--dark-color-lightness', darkColorLightness);
        root.style.setProperty('--white-color-lightness', whiteColorLightness);
    };

    Bg2.addEventListener('click', () => {
        darkColorLightness = '95%';
        lightColorLightness = '15%';
        whiteColorLightness = '20%';

        Bg2.classList.add('active');
        Bg1.classList.remove('active');
        Bg3.classList.remove('active');
        changeBg();
    });

    Bg3.addEventListener('click', () => {
        darkColorLightness = '95%';
        lightColorLightness = '10%';
        whiteColorLightness = '0%';

        Bg2.classList.remove('active');
        Bg1.classList.remove('active');
        Bg3.classList.add('active');
        changeBg();
    });

    Bg1.addEventListener('click', () => {
        Bg2.classList.remove('active');
        Bg1.classList.add('active');
        Bg3.classList.remove('active');
        window.location.reload(); // Reloads the page to reset to default light mode
    });
});

