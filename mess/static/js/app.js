// const button = document.getElementById('toggle-button');
// const cssLink = document.getElementById('css-link');

// button.addEventListener('click', () => {
//     const currentHref = cssLink.getAttribute('href');
//     const newHref = currentHref === "https://bootswatch.com/5/sketchy/bootstrap.min.css"
//         ? "https://bootswatch.com/5/sandstone/bootstrap.min.css"
//         : "https://bootswatch.com/5/sketchy/bootstrap.min.css";
//     cssLink.setAttribute('href', newHref);
// });




// New code

document.addEventListener('DOMContentLoaded', () => {
    const htmlElement = document.documentElement; // Reference to <html>
    const themeButtons = document.querySelectorAll('[data-bs-theme-value]'); // Theme buttons
    const savedTheme = localStorage.getItem('theme') || 'light'; // Default to light theme

    // Apply the saved theme
    htmlElement.setAttribute('data-bs-theme', savedTheme);

    // Update button states and classes for the saved theme
    function updateThemeButtons(selectedTheme) {
        themeButtons.forEach((button) => {
            const themeValue = button.getAttribute('data-bs-theme-value');
            const isActive = themeValue === selectedTheme;

            // Update aria-pressed attribute
            button.setAttribute('aria-pressed', isActive);

            // Toggle button class for active/inactive themes
            if (isActive) {
                button.classList.add('btn-dark'); // Add active theme class
                button.classList.remove('btn-light');
            } else {
                button.classList.add('btn-light'); // Revert to inactive style
                button.classList.remove('btn-dark');
            }
        });
    }

    // Initial setup for saved theme
    updateThemeButtons(savedTheme);

    // Add event listeners to theme buttons
    themeButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const themeValue = button.getAttribute('data-bs-theme-value');
            htmlElement.setAttribute('data-bs-theme', themeValue); // Apply the new theme

            // Save the selected theme to localStorage
            localStorage.setItem('theme', themeValue);

            // Update the buttons' styles and states
            updateThemeButtons(themeValue);
        });
    });
});



// // NEW UPDATE
// document.addEventListener('DOMContentLoaded', () => {
//     const toggleThemeButton = document.getElementById('toggle-theme');
//     const allElements = document.querySelectorAll('*'); // Select all elements in the DOM

//     // Function to toggle theme
//     function toggleTheme() {
//         allElements.forEach((el) => {
//             // Iterate through all attributes of the element
//             for (let attr of el.attributes) {
//                 if (attr.value.includes('dark') || attr.value.includes('light')) {
//                     // Replace 'dark' with 'light' and vice versa
//                     attr.value = attr.value
//                         .replace(/\bdark\b/gi, 'temp')
//                         .replace(/\blight\b/gi, 'dark')
//                         .replace(/\btemp\b/gi, 'light');
//                 }
//             }

//             // Update text content for occurrences of 'light' and 'dark'
//             el.childNodes.forEach((node) => {
//                 if (node.nodeType === Node.TEXT_NODE) {
//                     node.nodeValue = node.nodeValue
//                         .replace(/\blight\b/gi, 'temp')
//                         .replace(/\bdark\b/gi, 'light')
//                         .replace(/\btemp\b/gi, 'dark');
//                 }
//             });
//         });

//         // Update body background for better visual
//         document.body.classList.toggle('bg-dark');
//         document.body.classList.toggle('text-light');
//     }

//     // Add event listener to the button
//     toggleThemeButton.addEventListener('click', toggleTheme);
// });

