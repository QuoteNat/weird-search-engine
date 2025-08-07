class SearchController < ApplicationController
  def get
    @results = []
    params[:query].to_s.split(/\W+/) do |token|
      @results += Page.where("? = ANY(words)", token)
    end
  end
end
