odoo.define('car_report.dashboard', function (require) {
    "use strict";

    var core = require('web.core');
    var framework = require('web.framework');
    var session = require('web.session');
    var ajax = require('web.ajax');
    var ActionManager = require('web.ActionManager');
    var view_registry = require('web.view_registry');
    var Widget = require('web.Widget');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var QWeb = core.qweb;

    var _t = core._t;
    var _lt = core._lt;

    var CarReportView = AbstractAction.extend(ControlPanelMixin, {
        events: {
            'click .vehicle': 'action_vehicle',
            'click .payment': 'action_payment',
            'click .contract': 'action_contract',
            'click .customer': 'action_customer',
            /*'click #generate_payroll_pdf': function () {
                this.generate_payroll_pdf("bar");
            },
            'click #generate_attendance_pdf': function () {
                this.generate_payroll_pdf("pie")
            },
            'click .my_profile': 'action_my_profile',*/
        },
        init: function (parent, context) {
            this._super(parent, context);
            var car_data = [];
            var self = this;
            if (context.tag == 'car_report.dashboard') {
                self._rpc({
                    model: 'car.dashboard',
                    method: 'get_data_info',
                }, []).then(function (result) {
                    self.car_data = result[0];
                }).done(function () {
                    self.render();
                    self.href = window.location.href;
                });
            }
        },
        willStart: function () {
            return $.when(ajax.loadLibs(this), this._super());
        },
        start: function () {
            var self = this;
            return this._super();
        },
        render: function () {
            var super_render = this._super;
            var self = this;
            var car_report = QWeb.render('car_report.dashboard', {
                widget: self,
            });
            $(".o_control_panel").addClass("o_hidden");
            $(car_report).prependTo(self.$el);
            // self.graph();
            // self.previewTable();
            return car_report
        },
        reload: function () {
            window.location.href = this.href;
        },
        action_vehicle: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            return self.do_action({
                name: _t("Vehicles"),
                type: 'ir.actions.act_window',
                res_model: 'car.vehicle',
                view_mode: 'tree,form',
                view_type: 'form',
                views: [[false, 'list'], [false, 'form']],
                /*context: {
                    'search_default_employee_id': [self.employee_data.id],
                    'default_employee_id': self.employee_data.id,
                    'search_default_group_type': true,
                    'search_default_year': true
                },
                domain: [['holiday_type', '=', 'employee'], ['state', '!=', 'refuse']],
                search_view_id: self.employee_data.leave_search_view_id,*/
                target: 'current'
            }, {
                on_reverse_breadcrumb: function () {
                    return self.reload();
                }
            })
        },
        action_payment : function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            this.do_action({
                name: _t("Payments"),
                type: 'ir.actions.act_window',
                res_model: 'car.payment',
                view_mode: 'tree,form',
                view_type: 'form',
                views: [[false, 'list'], [false, 'form']],
                /*context: {
                    'search_default_employee_id': [self.employee_data.id],
                    'default_employee_id': self.employee_data.id,
                },*/
                target: 'current'
            }, {
                on_reverse_breadcrumb: function () {
                    return self.reload();
                }
            })
        },
        action_customer: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            this.do_action({
                name: _t("Customers"),
                type: 'ir.actions.act_window',
                res_model: 'res.partner',
                view_mode: 'tree,form',
                view_type: 'form',
                views: [[false, 'list'], [false, 'form']],
                /*context: {
                    'search_default_employee_id': [self.employee_data.id],
//                    'search_default_month': true,
                },
                domain: [['project_id', '!=', false]],*/
                target: 'current'
            }, {
                on_reverse_breadcrumb: function () {
                    return self.reload();
                }
            })
        },
        action_contract: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            this.do_action({
                name: _t("Contracts"),
                type: 'ir.actions.act_window',
                res_model: 'car.contract',
                view_mode: 'kanban,tree,form',
                view_type: 'form',
                views: [[false, 'kanban'], [false, 'list']],
                /*context: {
                    'search_default_employee_id': [self.employee_data.id],
                    'default_employee_id': self.employee_data.id,
                },*/
                target: 'current'
            }, {
                on_reverse_breadcrumb: function () {
                    return self.reload();
                }
            })
        },
        /*
        // Function which gives random color for charts.
        getRandomColor: function () {
            var letters = '0123456789ABCDEF'.split('');
            var color = '#';
            for (var i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        },
        // Here we are plotting bar,pie chart
        graph: function () {
            var self = this
            var ctx = this.$el.find('#myChart')
            // Fills the canvas with white background
            Chart.plugins.register({
                beforeDraw: function (chartInstance) {
                    var ctx = chartInstance.chart.ctx;
                    ctx.fillStyle = "white";
                    ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
                }
            });
            var bg_color_list = []
            for (var i = 0; i <= 12; i++) {
                bg_color_list.push(self.getRandomColor())
            }
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    //labels: ["January","February", "March", "April", "May", "June", "July", "August", "September",
                    // "October", "November", "December"],
                    labels: self.employee_data.payroll_label,
                    datasets: [{
                        label: 'Payroll',
                        data: self.employee_data.payroll_dataset,
                        backgroundColor: bg_color_list,
                        borderColor: bg_color_list,
                        borderWidth: 1,
                        pointBorderColor: 'white',
                        pointBackgroundColor: 'red',
                        pointRadius: 5,
                        pointHoverRadius: 10,
                        pointHitRadius: 30,
                        pointBorderWidth: 2,
                        pointStyle: 'rectRounded'
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: Math.max.apply(null, self.employee_data.payroll_dataset),
                                //min: 1000,
                                //max: 100000,
                                stepSize: self.employee_data.payroll_dataset.reduce((pv, cv) => {
                                        return pv + (parseFloat(cv) || 0)
                                    }, 0)
                                    / self.employee_data.payroll_dataset.length
                            }
                        }]
                    },
                    responsive: true,
                    maintainAspectRatio: true,
                    animation: {
                        duration: 100, // general animation time
                    },
                    hover: {
                        animationDuration: 500, // duration of animations when hovering an item
                    },
                    responsiveAnimationDuration: 500, // animation duration after a resize
                    legend: {
                        display: true,
                        labels: {
                            fontColor: 'black'
                        }
                    },
                },
            });
            //Pie Chart
            var piectx = this.$el.find('#attendanceChart');
            bg_color_list = []
            for (var i = 0; i <= self.employee_data.attendance_dataset.length; i++) {
                bg_color_list.push(self.getRandomColor())
            }
            var pieChart = new Chart(piectx, {
                type: 'pie',
                data: {
                    datasets: [{
                        data: self.employee_data.attendance_dataset,
                        backgroundColor: bg_color_list,
                        label: 'Attendance Pie'
                    }],
                    labels: self.employee_data.attendance_labels,
                },
                options: {
                    responsive: true
                }
            });

        },
        previewTable: function () {
            $('#emp_details').DataTable({
                dom: 'Bfrtip',
                buttons: [
                    'copy', 'csv', 'excel',
                    {
                        extend: 'pdf',
                        footer: 'true',
                        orientation: 'landscape',
                        title: 'Employee Details',
                        text: 'PDF',
                        exportOptions: {
                            modifier: {
                                selected: true
                            }
                        }
                    },
                    {
                        extend: 'print',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                    'colvis'
                ],
                columnDefs: [{
                    targets: -1,
                    visible: false
                }],
                lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
                pageLength: 15,
            });
        },
        generate_payroll_pdf: function (chart) {
            if (chart == 'bar') {
                var canvas = document.querySelector('#myChart');
            } else if (chart == 'pie') {
                var canvas = document.querySelector('#attendanceChart');
            }

            //creates image
            var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
            var doc = new jsPDF('landscape');
            doc.setFontSize(20);
            doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150);
            doc.save('report.pdf');
        },*/

    });
    core.action_registry.add('car_report.dashboard', CarReportView);
    return CarReportView
});