ymaps.ready(function () {
    var myMap = new ymaps.Map('map', {
        center: [55.755246, 37.617779],
        zoom: 9,
        controls: ['routePanelControl']
    });

    var control = myMap.controls.get('routePanelControl');

    control.routePanel.state.set({
        type: 'taxi',
        fromEnabled: true,
        from: 'Москва, Красная площадь, 1',
        toEnabled: true
    });

    control.routePanel.options.set({
        allowSwitch: false,
        reverseGeocoding: true,
        types: { taxi: true }
    });

    var switchPointsButton = new ymaps.control.Button({
        data: {content: "Поменять местами", title: "Поменять точки местами"},
        options: {selectOnClick: false, maxWidth: 160}
    });
    switchPointsButton.events.add('click', function () {
        control.routePanel.switchPoints();
    });
    myMap.controls.add(switchPointsButton);
});
