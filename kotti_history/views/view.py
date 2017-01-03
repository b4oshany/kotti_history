# -*- coding: utf-8 -*-

"""
Created on 2017-01-03
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from kotti import DBSession
from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti_history import _, fanstatic
from kotti_history.resources import ViewHistory, SearchHistory
from kotti_history.views import BaseView
from kotti_toolbox.decorators import (
    login_required
)


@view_config(
    name='history-recorder',
    renderer='kotti_history:templates/recorder.pt')
class RecorderView(BaseView):

    def __call__(self):
        return {
            "timeout": 5000
        }


class SearchHistoryView(BaseView):

    @view_config(name="save-search", root_only=True, permission="view",
                 decorator=(login_required), request_method="POST",
                 renderer="json")
    def save_search(self):
        term = self.request.params.get("term", "")
        if not term:
            return {
                "status": "Failed",
                "message": "No term sent"
            }
        SearchHistory.create(user_id=self.request.user.id, term=term)
        return dict(status="Success", message="{} has been added".format(term))


@view_defaults(name="history", context="kotti.resources.Content")
class Viewer(BaseView):

    @view_config(request_method="GET", renderer="json", permission="owner")
    def view_history(self):
        history = ViewHistory.find_by_content_id(self.context.id)
        return {
            "history": history
        }

    @view_config(request_method="POST", renderer="json", permission="view")
    def save_view_history(self):
        history = ViewHistory.find(content_id=self.context.id,
                                   user_id=self.request.user.id).one()
        if not history:
            ViewHistory.create(content=self.context, user=self.request.user)
            num_views = 1
        else:
            num_views = history.num_views + 1
            history.num_views = num_views
            DBSession.add(history)
        return {
            "status": "success",
            "message": "View count has been changed to {}".format(num_views)
        }
