var L = require('leaflet');
var _ = require('underscore');
var Spinner = require('spinjs');

var windowTemplate = require('livinglots.map.mail.window'),
    failureTemplate = require('livinglots.map.mail.failure'),
    successTemplate = require('livinglots.map.mail.success');

var cancelButtonSelector = '.mail-mode-cancel',
    submitButtonSelector = '.mail-mode-submit',
    formSelector = '.mail-mode-form';

L.Map.include({
    replaceMailWindowContent: function (content) {
        $('.map-mail-mode-container').remove();
        $(this.options.mailParent).append(content);
        this.fire('mailwindowchange');
    },

    sendMail: function () {
        var map = this,
            params = {},
            url = Django.url('lots:lot_email_organizers');

        _.extend(params, this.currentFilters, {
            bbox: this.getBounds().toBBoxString(),
            subject: $(formSelector).find(':input[name=subject]').val(),
            text: $(formSelector).find(':input[name=text]').val()
        });

        var spinner = new Spinner()
            .spin($(this.options.mailParent)[0]);

        $.getJSON(url + '?' + $.param(params))
            .always(function () {
                spinner.stop();
            })
            .done(function (data) {
                map.replaceMailWindowContent(successTemplate(data));
            })
            .fail(function (data) {
                map.replaceMailWindowContent(failureTemplate(data));
            });
    },

    mailSubmitDisabled: function (subject, text, emailCount) {
        return (subject === '' || text === '' || emailCount === 0);
    },

    updateMailWindow: function () {
        var map = this,
            params = {},
            url = Django.url('lots:lot_count_organizers');

        _.extend(params, this.currentFilters, {
            bbox: this.getBounds().toBBoxString()
        });

        var subject = $(formSelector).find(':input[name=subject]').val(),
            text = $(formSelector).find(':input[name=text]').val();
        $.getJSON(url + '?' + $.param(params), function (data) {
            _.extend(data, {
                disabled: map.mailSubmitDisabled(subject, text, data.emails),
                subject: subject,
                text: text
            });
            map.replaceMailWindowContent(windowTemplate(data));

            // Watch for changes on form to determine whether submit should be
            // enabled
            $(formSelector).find(':input').keyup(function () {
                var subject = $(formSelector).find(':input[name=subject]').val(),
                    text = $(formSelector).find(':input[name=text]').val(),
                    emails = $(formSelector).find(':input[name=emails]').val(),
                    disabled = map.mailSubmitDisabled(subject, text, emails);
                $(submitButtonSelector).prop('disabled', disabled);
            });
        });
    },

    enterMailMode: function () {
        $(this.options.mailParent).addClass('on');
        this.updateMailWindow();
        this.fire('entermode', { name: 'mail' });
        var map = this;

        // Update window on filters / map change
        this.on({
            'moveend': function () {
                map.updateMailWindow();
            },
            'zoomend': function () {
                map.updateMailWindow();
            }
        });

        this.on('entermode', function (data) {
            if (data.name !== 'mail') {
                map.exitMailMode();
            }
        });

        $('body').on('click', cancelButtonSelector, function (e) {
            map.exitMailMode();
            e.stopPropagation();
            return false;
        });

        $('body').on('click', submitButtonSelector, function (e) {
            // If already disabled, don't send mail
            if ($(submitButtonSelector).is('.disabled')) {
                return false;
            }
            $(submitButtonSelector).addClass('disabled');
            map.sendMail();
            e.stopPropagation();
            return false;
        });
    },

    exitMailMode: function () {
        $(this.options.mailParent).removeClass('on');
        $('.map-mail-mode-container').hide();
        this.fire('exitmode', { name: 'mail' });
    }
});
