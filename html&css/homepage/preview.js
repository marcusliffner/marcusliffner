document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('button');
    const duckSvg = document.getElementById('duck-svg');

    // Define a mapping between color names and their corresponding fill colors
    const colorcode =
    {
        'Primary': 'Blue',
        'Secondary': 'Grey',
        'Success': 'Green',
        'Danger': 'Red',
        'Warning': 'Orange',
        'Info': 'lightblue',
        'Light': 'lightgrey',
        'Dark': 'black',
        'Original': 'yellow'
    };
    const personalities =
    {
        'Primary': 'The adventurous explorer. This duck is always ready to embark on new journeys, discovering hidden wonders and overcoming challenges along the way.',
        'Secondary': 'The calm and collected thinker. Known for its contemplative nature, this duck approaches situations with a thoughtful mind, finding solutions with ease.',
        'Success': 'The optimistic achiever. With a positive outlook on life, this duck strives for success in all endeavors, inspiring others with its determination.',
        'Danger': 'The bold and daring risk-taker. Fearless and adventurous, this duck thrives on taking risks and embraces the excitement of the unknown.',
        'Warning': 'The cautious strategist. Methodical and calculated, this duck carefully plans its moves, always considering the potential consequences before taking action.',
        'Info': 'The curious and knowledgeable learner. Constantly seeking knowledge, this duck is a natural scholar, eager to explore and understand the world around it.',
        'Light': 'The gentle and caring soul. Radiating warmth and kindness, this duck brings comfort and support to those around it, creating a harmonious environment.',
        'Dark': 'The enigmatic and stealthy character. Cloaked in mystery, this duck moves with an air of intrigue, leaving others captivated by its unique and unpredictable nature, much like a ninja mastering the shadows.',
        'Original': 'The one and only original duck. This duck is a symbol of individuality, embracing its distinct qualities that set it apart from the rest.'
    };

    buttons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            let colorName = button.getAttribute('data-color');

            const fillColor = colorcode[colorName] || colorcode['Original'];
            const personality = personalities[colorName] || personalities['Original'];

            document.getElementById('duckname').innerHTML = colorName;
            document.getElementById('duckattribute').innerHTML = personality;

            duckSvg.getElementById('svg_3').setAttribute('fill', fillColor);
            duckSvg.getElementById('svg_4').setAttribute('fill', fillColor);
            duckSvg.getElementById('svg_18').setAttribute('fill', fillColor);
            duckSvg.getElementById('svg_19').setAttribute('fill', fillColor);

            event.preventDefault();
        });
    });
});