from typing import Any, List

from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Query, Session

from app.schema import FilterRequestSchema


class DBUtils:
    @staticmethod
    def build_query(request_filters: Any, query_model: Any) -> list:
        filter_list = []
        sort_orders = []
        if (request_filters.search_key and len(request_filters.search_key) > 0) and (
                request_filters.search_text and len(request_filters.search_text) > 0
        ):
            filter_list.append(
                getattr(query_model, request_filters.search_key).like("%" + request_filters.search_text + "%")
            )
        for filters in request_filters.filters:
            if filters.operator.lower() == "in" and len(filters.values) > 0:
                filter_list.append(
                    getattr(query_model, filters.field).in_(filters.values)
                )
            if (
                    filters.operator.lower() == "notin"
                    or filters.operator.lower() == "not in"
                    or filters.operator.lower() == "nin"
            ) and len(filters.values) > 0:
                filter_list.append(
                    getattr(query_model, filters.field).not_in(tuple(filters.values))
                )
            if filters.operator.lower() == "like":
                filter_list.append(
                    getattr(query_model, filters.field).like("%" + filters.values[0] + "%")
                )
            if filters.operator.lower() == "between":
                filter_list.append(
                    getattr(query_model, filters.field).between(
                        filters.values[0], filters.values[1]
                    )
                )
        for sort in request_filters.sort:
            if sort.order.lower() == "asc":
                sort_orders.append(getattr(query_model, sort.field).asc())
            if sort.order.lower() == "desc":
                sort_orders.append(getattr(query_model, sort.field).desc())
        return [filter_list, sort_orders]

    @classmethod
    def make_query(
            cls,
            filters: FilterRequestSchema,
            session: Session,
            query_model: Any,
            pre_query: Any = None,
            additional_filters: List = None
    ) -> [Query, Query]:
        query = pre_query
        if query is None:
            query = session.query(query_model)
        if additional_filters:
            query = query.filter(*additional_filters)
        query_filters, sort_orders = cls.build_query(
            filters,
            query_model=query_model,
        )
        total_count = query.count()
        if filters.page_info.start > 0 and filters.page_info.rows > 0:
            query = (
                query.filter(and_(*query_filters))
                .order_by(*sort_orders)
                .offset(filters.page_info.start)
                .limit(filters.page_info.rows)
            )
        elif filters.page_info.start > 0:
            query = (
                query.filter(and_(*query_filters))
                .order_by(*sort_orders)
                .offset(filters.page_info.start)
            )

        elif filters.page_info.rows > 0:
            query = (
                query.filter(and_(*query_filters))
                .order_by(*sort_orders)
                .limit(filters.page_info.rows)
            )
        else:
            query = query.filter(and_(*query_filters)).order_by(*sort_orders)
        return query, total_count
