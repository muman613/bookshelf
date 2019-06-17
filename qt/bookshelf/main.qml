import QtQuick 2.7
import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.4

Window {
    id: mainwindow
    visible: true
    width: 1200
    height: 480
    color: 'aqua'
    title: qsTr("BookShelf QML App")

    ListModel {
        id: listmodel
    }

    ListView {
        anchors.margins: 32
        id: listview
        anchors.fill: parent
        model: listmodel
        delegate: Rectangle {
            width: parent.width
            height: rowlayout.implicitHeight
            color: mainwindow.color
            RowLayout {
                id: rowlayout
                anchors.fill: parent
//                Text {
//                    text: isbn
//                    font.pointSize: 32
//                }
                Text {
                    font.family: "Mono"
                    font.pointSize: 12


                    text: title.padEnd(50, ' ') + " " + author.padEnd(80, ' ')
//                    font.pointSize: 12
                }
            }
        }

        ScrollBar.vertical: ScrollBar {

        }
    }

    function request() {
        var xhr = new XMLHttpRequest();
        print('request');

        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.HEADERS_RECEIVED) {
//                print('Headers received!');
            } else if (xhr.readyState === XMLHttpRequest.DONE) {
                var obj = JSON.parse(xhr.responseText.toString());
                obj.forEach(function (item, index) {
                    listmodel.append(item);
                });
                // This is available in all editors.
            }
        }

        xhr.open("GET", "http://localhost:8000/api/books")
        xhr.send()


    }

    Component.onCompleted: {
//        var JsonString = '{"a":"A whatever, run","b":"B fore something happens"}';
//        var JsonObject= JSON.parse(JsonString);

//        //retrieve values from JSON again
//        var aString = JsonObject.a;
//        var bString = JsonObject.b;

//        console.log(JsonObject.a);
//        console.log(bString);

        request();
    }
}
